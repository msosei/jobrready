(async () => {
  const { apiUrl } = await chrome.storage.sync.get('apiUrl')
  console.log('Content script active. API:', apiUrl)
  // Placeholder: detect forms and autofill if enabled
})()


