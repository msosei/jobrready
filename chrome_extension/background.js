chrome.runtime.onInstalled.addListener(() => {
  console.log('MyBrand extension installed')
})

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'PING') {
    sendResponse({ ok: true })
  }
})


