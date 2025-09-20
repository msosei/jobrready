const apiUrlEl = document.getElementById('apiUrl')
const statusEl = document.getElementById('status')
document.getElementById('save').addEventListener('click', async () => {
  const apiUrl = apiUrlEl.value || 'http://localhost:8000'
  await chrome.storage.sync.set({ apiUrl })
  statusEl.textContent = 'Saved'
  setTimeout(() => (statusEl.textContent = 'Idle'), 1000)
})


