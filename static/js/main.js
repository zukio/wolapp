// PC状態の更新間隔（ミリ秒）
const UPDATE_INTERVAL = 5000;

// PC一覧を更新
function updatePCs() {
  fetch("/status")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("pc-container");
      container.innerHTML = "";

      for (const [pcId, pc] of Object.entries(data)) {
        const card = document.createElement("div");
        card.className = "pc-card";

        // ステータスクラスの決定
        let statusClass = "status-unknown";
        let statusText = "不明";
        let spinnerHtml = "";

        switch (pc.status) {
          case "online":
            statusClass = "status-online";
            statusText = "オンライン";
            break;
          case "offline":
            statusClass = "status-offline";
            statusText = "オフライン";
            break;
          case "waking":
            statusClass = "status-waking";
            statusText = "起動中";
            spinnerHtml = '<span class="spinner"></span>';
            break;
          case "shuttingdown":
            statusClass = "status-shuttingdown";
            statusText = "シャットダウン中";
            spinnerHtml = '<span class="spinner"></span>';
            break;
        }

        // ボタンの有効/無効状態
        const wakeDisabled = pc.status === "online" || pc.status === "waking" || pc.status === "shuttingdown";
        const shutdownDisabled = pc.status !== "online" || pc.status === "waking" || pc.status === "shuttingdown";

        card.innerHTML = `
                    <div class="pc-header">
                        <div class="pc-name">${pc.name}</div>
                        <div class="pc-status ${statusClass}">${spinnerHtml}${statusText}</div>
                    </div>
                    <div class="pc-info">
                        <div>IP: ${pc.ip}</div>
                        <div>MAC: ${pc.mac}</div>
                    </div>
                    <div class="pc-actions">
                        <button class="wake-btn" onclick="wakePc('${pcId}')" ${wakeDisabled ? "disabled" : ""}>起動</button>
                        <button class="shutdown-btn" onclick="shutdownPc('${pcId}')" ${shutdownDisabled ? "disabled" : ""}>シャットダウン</button>
                    </div>
                `;

        container.appendChild(card);
      }
    })
    .catch((error) => console.error("更新エラー:", error));
}

// Wake on LAN実行
function wakePc(pcId) {
  fetch(`/wake/${pcId}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message);
      updatePCs();
    })
    .catch((error) => console.error("起動エラー:", error));
}

// シャットダウン実行
function shutdownPc(pcId) {
  if (confirm("このPCをシャットダウンしますか？")) {
    fetch(`/shutdown/${pcId}`, {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        updatePCs();
      })
      .catch((error) => console.error("シャットダウンエラー:", error));
  }
}

// アプリケーションを終了
function closeApp() {
  if (confirm("アプリケーションを終了しますか？")) {
    fetch("/exit", {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message);
        // 終了メッセージを表示
        const container = document.getElementById("pc-container");
        container.innerHTML = '<div class="exit-message">アプリケーションを終了しています...</div>';
      })
      .catch((error) => console.error("終了エラー:", error));
  }
}

// 初期表示と定期更新
updatePCs();
setInterval(updatePCs, UPDATE_INTERVAL);

// Closeボタンのイベントリスナーを設定
document.addEventListener("DOMContentLoaded", function () {
  const closeBtn = document.getElementById("close-app-btn");
  if (closeBtn) {
    closeBtn.addEventListener("click", closeApp);
  }
});
