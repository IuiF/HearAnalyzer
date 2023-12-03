import spacy
import six
from google.cloud import translate_v2 as translate


class TextAnalyzer:
    def __init__(self, model_name="en_core_web_sm"):
        self.nlp = spacy.load(model_name)
        self.dep_labels_ja = {
            "acl": "名詞の修飾節",
            "advcl": "副詞節の修飾",
            "advmod": "副詞的修飾",
            "amod": "形容詞的修飾",
            "appos": "同格の修飾",
            "aux": "助動詞",
            "case": "格標識",
            "cc": "並列接続詞",
            "ccomp": "節の補完",
            "clf": "分類詞",
            "compound": "複合語",
            "conj": "接続詞",
            "cop": "連語動詞",
            "csubj": "節の主語",
            "dep": "未指定の依存関係",
            "det": "冠詞",
            "discourse": "談話要素",
            "dislocated": "非通常の配置",
            "expl": "仮想の主語",
            "fixed": "固定の句",
            "flat": "平文の句",
            "goeswith": "関連語",
            "iobj": "間接目的語",
            "list": "リスト",
            "mark": "標識",
            "nmod": "名詞の修飾",
            "nsubj": "名詞の主語",
            "nummod": "数詞の修飾",
            "obj": "目的語",
            "obl": "斜格名詞",
            "orphan": "孤立",
            "parataxis": "並列構造",
            "punct": "句読点",
            "prep": "前置詞",
            "pobj": "前置詞の目的語",
            "reparandum": "修正文",
            "ROOT": "文のルート",
            "vocative": "呼格",
            "xcomp": "節の補完",
        }

        self.pos_tags_ja = {
            "ADJ": "形容詞",
            "ADP": "前置詞",
            "ADV": "副詞",
            "AUX": "助動詞",
            "CCONJ": "接続詞",
            "DET": "冠詞",
            "INTJ": "間投詞",
            "NOUN": "名詞",
            "NUM": "数詞",
            "PART": "助詞",
            "PRON": "代名詞",
            "PROPN": "固有名詞",
            "PUNCT": "句読点",
            "SCONJ": "従属接続詞",
            "SYM": "記号",
            "VERB": "動詞",
            "X": "その他",
        }

    def analyze(self, text):
        doc = self.nlp(text)
        results = {"tokens": [], "pos_tags": [], "dependencies": []}

        for token in doc:
            # 依存関係と品詞タグを日本語に変換
            dep_label_ja = self.dep_labels_ja.get(token.dep_, token.dep_)
            pos_tag_ja = self.pos_tags_ja.get(token.pos_, token.pos_)
            results["tokens"].append(token.text)
            results["pos_tags"].append(pos_tag_ja)
            results["dependencies"].append(
                {"token": token.text, "head": token.head.text, "dep": dep_label_ja}
            )

        return results

    def translator(self, text):
        # Translate Clientの生成
        translate_client = translate.Client()

        # 英語テキストを日本語に翻訳
        translation = translate_client.translate(text, target_language="ja")
        translated_text = translation["translatedText"]

        return translated_text
