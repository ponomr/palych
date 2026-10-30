"""Tests for the reply shape metrics; all replies are synthetic."""
import importlib.util
import json
import re
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("shape_metrics", Path(__file__).with_name("shape_metrics.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

KEYS = json.loads(Path(__file__).with_name("answer-keys.json").read_text(encoding="utf-8"))["keys"]

STATED = "Кэш здесь не помогает: поиск занимает 10 мс, а вычисление 2 мс.\n\nДругих измерений нет."
BURIED = ("Хороший вопрос. Сначала разберёмся, что такое кэш и зачем он нужен. "
          "Кэш хранит готовые результаты. В этом случае он не помогает, потому что поиск дольше.\n\n"
          "Если хотите, могу объяснить подробнее.")


def record(case_id, condition, response, repetition=1):
    return {"case_id": case_id, "repetition": repetition, "condition": condition, "response": response}


class MeasureTests(unittest.TestCase):
    def test_point_in_first_sentence(self):
        row = mod.measure(STATED, KEYS["ru-cost"])
        self.assertTrue(row["point_first"])
        self.assertEqual(row["to_point"], 2)
        self.assertFalse(row["opener"] or row["closer"])

    def test_buried_point_and_ceremony(self):
        row = mod.measure(BURIED, KEYS["ru-cost"])
        self.assertFalse(row["point_first"])
        self.assertGreater(row["to_point"], 10)
        self.assertTrue(row["opener"] and row["closer"])

    def test_missing_point_counts_whole_reply(self):
        row = mod.measure("Всё зависит от обстоятельств.", KEYS["ru-cost"])
        self.assertFalse(row["point_found"])
        self.assertEqual(row["to_point"], 4)

    def test_case_without_key_has_no_point_fields(self):
        self.assertNotIn("to_point", mod.measure(STATED, None))

    def test_first_sentence_skips_heading_and_list_marker(self):
        text = "## Итог\n\n1. Тариф Д — 300 ₽. Он дешевле всех с 8 ГБ.\n2. Тариф Е — 400 ₽."
        row = mod.measure(text, KEYS["ru-seven"])
        self.assertTrue(row["point_first"])
        self.assertEqual(row["to_point"], 3)
        self.assertEqual(row["headings"], 1)

    def test_labels_and_greeting_are_not_the_first_sentence(self):
        labelled = "**Срок.** Отправить нужно до 21 ноября, 09:40. Опоздание не описано."
        self.assertTrue(mod.measure(labelled, KEYS["ru-deadline"])["point_first"])
        titled = "**Submission rules**\n\n- **Deadline:** submit before 21 November."
        self.assertTrue(mod.measure(titled, KEYS["en-deadline"])["point_first"])
        letter = "Здравствуйте!\n\nНа странице тарифов указано 900 ₽ в месяц."
        self.assertTrue(mod.measure(letter, KEYS["ru-price-conflict"])["point_first"])

    def test_bold_statement_is_still_a_sentence(self):
        start, end = mod.first_sentence_span("**Use the cache.**\n\nIt is faster.")
        self.assertEqual(end, len("**Use the cache.**"))
        self.assertTrue(mod.measure("**No.** The lookup takes 10 ms.", KEYS["en-cost"])["point_first"])

    def test_warm_up_line_is_the_first_sentence(self):
        text = "Простыми словами это звучит так:\n\nВерсию советуют, но ставить необязательно."
        self.assertFalse(mod.measure(text, KEYS["ru-unknown-reason"])["point_first"])

    def test_decimal_point_does_not_end_sentence(self):
        start, end = mod.first_sentence_span("The invoice says $9.90 and the page says $9. Ask billing.")
        self.assertEqual(end, len("The invoice says $9.90 and the page says $9."))

    def test_list_items_are_separate_blocks(self):
        text = "Шаги:\n- первый шаг из трёх слов\n- второй\n\nОдин длинный абзац из семи слов здесь."
        self.assertEqual(mod.measure(text)["longest_block"], 7)

    def test_wrapper_and_ceremonial_opener(self):
        self.assertTrue(mod.measure("Here's a draft:\n\nThe filter is in.")["wrapper"])
        self.assertTrue(mod.measure("Sure! The filter is in.")["opener"])
        self.assertFalse(mod.measure("The filter is in.")["wrapper"])

    def test_case_sensitive_plan_letter(self):
        self.assertIsNone(re.search(KEYS["en-seven"], "Cheapest, e.g. by total."))
        self.assertIsNotNone(re.search(KEYS["en-seven"], "Plan E costs $30."))

    def test_blocking_question_flagged_first_and_asked_last(self):
        text = ("Нужно ваше решение по 20 заказам с валютой `RUR`. Перенесено 1180 из 1200.\n\n"
                "Заменить `RUR` на `RUB` или оставить эти 20 заказов в старой базе?")
        row = mod.measure(text, KEYS["ru-block-currency"])
        self.assertTrue(row["point_first"])
        self.assertEqual(row["questions"], 1)
        self.assertTrue(row["question_last"])
        self.assertEqual(row["after_question"], 0)

    def test_question_buried_mid_reply(self):
        text = ("1180 of 1200 orders are moved. Should I replace `RUR` with `RUB` or leave them? "
                "Let me know and I will finish.")
        row = mod.measure(text, KEYS["en-block-currency"])
        self.assertFalse(row["point_first"])
        self.assertFalse(row["question_last"])
        self.assertEqual(row["after_question"], 7)
        self.assertTrue(row["closer"])

    def test_reply_without_question_and_url_query(self):
        row = mod.measure("Report saved; see https://x.test/r?id=1 for details.")
        self.assertEqual(row["questions"], 0)
        self.assertNotIn("question_last", row)


DELIVERABLES = json.loads(Path(__file__).with_name("answer-keys.json").read_text(encoding="utf-8"))["deliverables"]


class WrappingTests(unittest.TestCase):
    def test_bare_commit_message_in_a_fence_is_pure(self):
        text = "```\ninvoice: round the total once\n\nTotals differed by 1–2 cents.\n\nRefs: #214\n```"
        row = mod.measure(text, None, DELIVERABLES["en-commit"])
        self.assertTrue(row["pure_text"])
        self.assertEqual((row["lead_in"], row["tail"]), (0, 0))

    def test_lead_in_and_tail_around_a_letter(self):
        text = ("Вот письмо клиенту:\n\nЗдравствуйте, Иван!\n\nЗаказ № 4821 приедет 15 ноября.\n\n"
                "С уважением,\nАнна, отдел доставки\n\nЕсли нужно, сделаю короче.")
        row = mod.measure(text, None, DELIVERABLES["ru-letter"])
        self.assertFalse(row["pure_text"])
        self.assertEqual(row["lead_in"], 3)
        self.assertEqual(row["tail"], 4)
        self.assertTrue(row["wrapper"] and row["closer"])

    def test_text_without_fixed_end_and_missing_text(self):
        row = mod.measure("Марина, привет! Созвон в четверг в 15:00.", None, DELIVERABLES["ru-chat"])
        self.assertTrue(row["pure_text"])
        self.assertNotIn("tail", row)
        self.assertFalse(mod.measure("Готово.", None, DELIVERABLES["ru-notice"])["text_found"])

    def test_text_shares(self):
        records = [record("en-commit", "skill", "invoice: round once\n\nRefs: #214"),
                   record("en-commit", "skill", "Here you go:\n\ninvoice: round once\n\nRefs: #214", 2),
                   record("en-commit", "skill", "Done.", 3)]
        summary = mod.evaluate(records, KEYS, deliverables=DELIVERABLES)[("skill", None)]
        self.assertEqual((summary["texts"], summary["text_missed"]), (2, 1))
        self.assertEqual(summary["pure_text"], 0.5)
        self.assertEqual((summary["lead_in"], summary["tail"]), (0.5, 0.0))


class EvaluateTests(unittest.TestCase):
    def test_buried_control_scores_worse_than_its_source(self):
        records = [record("ru-cost", "skill", STATED),
                   record("en-cost", "skill", "No: the lookup takes 10 ms.\n\n- lookup 10 ms\n- compute 2 ms")]
        results = mod.evaluate(records, KEYS, control="skill")
        stated, buried = results[("skill", None)], results[("skill+buried", None)]
        self.assertEqual(stated["point_first"], 1.0)
        self.assertEqual(buried["point_first"], 0.0)
        self.assertGreater(buried["to_point"], stated["to_point"])
        self.assertGreater(buried["longest_block"], stated["longest_block"])
        self.assertEqual(buried["opener"], 1.0)

    def test_split_and_unkeyed_cases(self):
        records = [record("ru-depth", "skill", "Процесс из четырёх этапов."),
                   record("en-cost", "skill", "No.")]
        results = mod.evaluate(records, KEYS, split="language")
        self.assertEqual(results[("skill", "ru")]["keyed"], 0)
        self.assertIsNone(results[("skill", "ru")]["point_first"])
        self.assertEqual(results[("skill", "en")]["point_first"], 1.0)

    def test_question_shares_count_only_replies_that_ask(self):
        records = [record("en-block-date", "skill", "Which date is correct, 14 or 15 November?"),
                   record("en-block-date", "skill", "Which date is correct? Reply when you can.", 2),
                   record("en-noblock-done", "skill", "All 1200 orders are moved.")]
        summary = mod.evaluate(records, KEYS)[("skill", None)]
        self.assertEqual(summary["asked"], 0.667)
        self.assertEqual(summary["question_last"], 0.5)
        self.assertEqual(summary["after_question"], 2)


if __name__ == "__main__":
    unittest.main()
