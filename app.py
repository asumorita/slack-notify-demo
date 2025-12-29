import streamlit as st
import requests
import json
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="Slack通知デモ",
    page_icon="📱",
    layout="wide"
)

# セッション状態の初期化
if 'notification_log' not in st.session_state:
    st.session_state.notification_log = []

# タイトル
st.title("📱 Slack通知デモ")
st.write("通知を送る仕組みを学びます（後で本物のSlackに接続可能）")

# タブで機能を分ける
tab1, tab2, tab3 = st.tabs(["📝 基本通知", "💰 物販通知", "📊 ログ"])

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ1: 基本通知
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.header("📝 基本通知のデモ")
    
    st.info("💡 Slack Webhook URLを入れると本物の通知が送れます。今は空欄でOK（デモモード）")
    
    # Webhook URL入力（オプション）
    webhook_url = st.text_input(
        "Slack Webhook URL（オプション）",
        placeholder="https://hooks.slack.com/services/...",
        type="password"
    )
    
    st.divider()
    
    # 簡単な通知
    st.subheader("例1: シンプルな通知")
    
    message1 = st.text_input("メッセージを入力", value="テスト通知です！", key="msg1")
    
    if st.button("📤 通知を送る", key="send1"):
        if webhook_url:
            # 本物のSlackに送信
            try:
                payload = {"text": message1}
                response = requests.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    st.success("✅ Slackに通知を送信しました！")
                else:
                    st.error(f"❌ エラー: {response.status_code}")
            except Exception as e:
                st.error(f"❌ エラー: {str(e)}")
        else:
            # デモモード
            st.success("✅ 通知を送信しました！（デモモード）")
            st.info(f"📱 送信内容: {message1}")
        
        # ログに記録
        st.session_state.notification_log.append({
            "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "種類": "シンプル通知",
            "内容": message1,
            "状態": "成功" if webhook_url else "デモ"
        })
    
    st.divider()
    
    # リッチな通知
    st.subheader("例2: リッチな通知（タイトル付き）")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title2 = st.text_input("タイトル", value="重要なお知らせ", key="title2")
    
    with col2:
        message2 = st.text_area("メッセージ", value="売上が目標を達成しました！", key="msg2")
    
    if st.button("📤 リッチ通知を送る", key="send2"):
        if webhook_url:
            # 本物のSlackに送信
            try:
                payload = {
                    "text": title2,
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": title2
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": message2
                            }
                        }
                    ]
                }
                response = requests.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    st.success("✅ Slackに通知を送信しました！")
                else:
                    st.error(f"❌ エラー: {response.status_code}")
            except Exception as e:
                st.error(f"❌ エラー: {str(e)}")
        else:
            # デモモード
            st.success("✅ リッチ通知を送信しました！（デモモード）")
            st.info(f"📱 **{title2}**\n\n{message2}")
        
        # ログに記録
        st.session_state.notification_log.append({
            "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "種類": "リッチ通知",
            "内容": f"{title2}: {message2}",
            "状態": "成功" if webhook_url else "デモ"
        })

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ2: 物販通知
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.header("💰 物販関連の通知")
    
    st.subheader("例1: 売上通知")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        product_name = st.text_input("商品名", value="商品A", key="prod1")
    
    with col2:
        sale_price = st.number_input("販売価格", value=5000, key="price1")
    
    with col3:
        profit = st.number_input("利益", value=1500, key="profit1")
    
    if st.button("📤 売上通知を送る", key="send3"):
        notification_text = f"""
🎉 商品が売れました！

商品名: {product_name}
販売価格: ¥{sale_price:,}
利益: ¥{profit:,}
利益率: {(profit/sale_price*100):.1f}%

おめでとうございます！
"""
        
        if webhook_url:
            # 本物のSlackに送信
            try:
                payload = {
                    "text": "商品が売れました！",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "🎉 商品が売れました！"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*商品名:*\n{product_name}"},
                                {"type": "mrkdwn", "text": f"*販売価格:*\n¥{sale_price:,}"},
                                {"type": "mrkdwn", "text": f"*利益:*\n¥{profit:,}"},
                                {"type": "mrkdwn", "text": f"*利益率:*\n{(profit/sale_price*100):.1f}%"}
                            ]
                        }
                    ]
                }
                response = requests.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    st.success("✅ Slackに売上通知を送信しました！")
                else:
                    st.error(f"❌ エラー: {response.status_code}")
            except Exception as e:
                st.error(f"❌ エラー: {str(e)}")
        else:
            # デモモード
            st.success("✅ 売上通知を送信しました！（デモモード）")
            st.info(notification_text)
        
        # ログに記録
        st.session_state.notification_log.append({
            "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "種類": "売上通知",
            "内容": f"{product_name} - ¥{profit:,}",
            "状態": "成功" if webhook_url else "デモ"
        })
    
    st.divider()
    
    st.subheader("例2: エラー通知")
    
    error_type = st.selectbox(
        "エラーの種類",
        ["在庫切れ", "価格エラー", "API接続エラー", "システムエラー"]
    )
    
    error_detail = st.text_area("エラー詳細", value="詳細情報をここに入力", key="error1")
    
    if st.button("📤 エラー通知を送る", key="send4"):
        notification_text = f"""
⚠️ エラーが発生しました

種類: {error_type}
詳細: {error_detail}
発生時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

確認をお願いします。
"""
        
        if webhook_url:
            # 本物のSlackに送信
            try:
                payload = {
                    "text": "エラーが発生しました",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "⚠️ エラーが発生しました"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {"type": "mrkdwn", "text": f"*種類:*\n{error_type}"},
                                {"type": "mrkdwn", "text": f"*発生時刻:*\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*詳細:*\n{error_detail}"
                            }
                        }
                    ]
                }
                response = requests.post(webhook_url, json=payload)
                
                if response.status_code == 200:
                    st.success("✅ Slackにエラー通知を送信しました！")
                else:
                    st.error(f"❌ エラー: {response.status_code}")
            except Exception as e:
                st.error(f"❌ エラー: {str(e)}")
        else:
            # デモモード
            st.warning("✅ エラー通知を送信しました！（デモモード）")
            st.info(notification_text)
        
        # ログに記録
        st.session_state.notification_log.append({
            "時刻": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "種類": "エラー通知",
            "内容": f"{error_type}: {error_detail}",
            "状態": "成功" if webhook_url else "デモ"
        })

# ━━━━━━━━━━━━━━━━━━━━━━━━
# タブ3: 通知ログ
# ━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.header("📊 通知ログ")
    
    if len(st.session_state.notification_log) == 0:
        st.info("まだ通知を送っていません")
    else:
        st.write(f"合計 {len(st.session_state.notification_log)} 件の通知")
        
        import pandas as pd
        df_log = pd.DataFrame(st.session_state.notification_log)
        st.dataframe(df_log, use_container_width=True)
        
        # CSVダウンロード
        csv = df_log.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 ログをCSVでダウンロード",
            data=csv,
            file_name=f"notification_log_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        # ログクリア
        if st.button("🗑️ ログをクリア"):
            st.session_state.notification_log = []
            st.rerun()

# サイドバー
st.sidebar.header("💡 使い方")

st.sidebar.info("""
**デモモード（今）**
- Webhook URL無しで動作
- 通知のシミュレーション
- 学習用

**本番モード（後で）**
1. Slack Webhook URLを取得
2. 上部の入力欄に貼り付け
3. 実際にSlackに通知が届く

**次のステップ（レベル30-40）**
- LINE Messaging APIに挑戦
- LINEに通知を送る
""")

st.sidebar.divider()

st.sidebar.success("""
**物販での使い方**
- 商品が売れたら通知
- 在庫切れを通知
- 価格変動を通知
- エラーを即座に通知
""")

st.sidebar.divider()

# 統計
st.sidebar.metric("通知送信回数", len(st.session_state.notification_log))
