import pandas as pd
import gradio as gr
import io

# --- CSV読込と検索機能 ---
def load_csv(file):
    if file is None:
        return "ファイルを選択してください", None
    df = pd.read_csv(file.name if hasattr(file, "name") else io.StringIO(file.decode("utf-8")))
    df_html = df.head(10).to_html(index=False)
    return f"読み込み完了: {len(df)} 行", df_html

def search_csv(file, keyword):
    if file is None:
        return "先にCSVを読み込んでください", None
    df = pd.read_csv(file.name if hasattr(file, "name") else io.StringIO(file.decode("utf-8")))
    if not keyword.strip():
        return "キーワードを入力してください", None
    result = df[df.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]
    if result.empty:
        return "該当する行はありません。", None
    return f"ヒット件数: {len(result)} 行", result.head(10).to_html(index=False)

# --- Gradio UI構築 ---
with gr.Blocks(title="CSV 検索アプリ（Gradio版）") as demo:
    gr.Markdown("## 📄 CSV検索＆プレビュー（Gradio版）\nCSVをアップロードして検索できます。")
    
    csv_file = gr.File(label="CSVファイルを選択")
    keyword = gr.Textbox(label="🔎 検索キーワード", placeholder="キーワードを入力")
    
    btn_load = gr.Button("📂 CSVを読み込む")
    load_info = gr.Textbox(label="ステータス")
    load_table = gr.HTML()
    
    btn_search = gr.Button("🔍 検索を実行")
    search_info = gr.Textbox(label="検索結果")
    search_table = gr.HTML()

    btn_load.click(load_csv, inputs=csv_file, outputs=[load_info, load_table])
    btn_search.click(search_csv, inputs=[csv_file, keyword], outputs=[search_info, search_table])

# --- 起動 ---
if __name__ == "__main__":
    demo.launch(share=True, inbrowser=True)