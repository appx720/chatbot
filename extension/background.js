let keepRunning = true;
let isProcessing = false;

async function checkServerAndSend() {
  if (!keepRunning || isProcessing) return;

  isProcessing = true; // 🔒 처리 중

  try {
    const res = await fetch("http://localhost:8000/send");
    const data = await res.json();

    if (data.send) {
      const oneHourAgo = Date.now() - 1000 * 60 * 60;
      chrome.history.search({ text: '', startTime: oneHourAgo, maxResults: 50 }, (items) => {
        const logs = items.map(item => ({ url: item.url }));

        fetch("http://localhost:8000/log", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(logs)
        }).then(() => {
          return fetch("http://localhost:8000/done", { method: "POST" });
        }).catch(err => console.error("🚫 전송 실패:", err))
          .finally(() => {
            isProcessing = false; // 🔓 해제
          });
      });
    } else {
      isProcessing = false; // 🔓 해제 (send가 false인 경우도)
    }
  } catch (err) {
    console.error("❌ 서버 요청 실패:", err);
    isProcessing = false; // 🔓 예외 발생 시도 해제
  }

  setTimeout(checkServerAndSend, 10000);  // 10초 후 반복
}

// 확장 설치될 때 시작
chrome.runtime.onInstalled.addListener(() => {
  keepRunning = true;
  checkServerAndSend();
});

// 브라우저 시작 시에도 시작
chrome.runtime.onStartup.addListener(() => {
  keepRunning = true;
  checkServerAndSend();
});

// 안전망 알람
chrome.alarms.create('safetyNet', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'safetyNet') {
    console.log("🔁 알람 wake-up");
    checkServerAndSend();
  }
});
