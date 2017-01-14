export function loadCache(key) {
  try {
    const raw = localStorage.getItem(key);
    return raw && JSON.parse(raw);
  } catch (e) {
    localStorage.removeItem(key);
  }
}

export function dumpCache(key, data) {
  if (data) {
    localStorage.setItem(key, JSON.stringify(data));
  } else {
    localStorage.removeItem(key);
  }
}
