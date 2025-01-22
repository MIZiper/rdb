export function getTagColor(tag) {
  const tagCategory = tag.split(':')[0];
  const hash = Math.abs(hashString(tagCategory));
  const colors = ['red', 'pink', 'purple', 'deep-purple', 'indigo', 'blue', 'light-blue', 'cyan', 'teal', 'green', 'light-green', 'lime', 'orange', 'deep-orange', 'brown', 'grey', 'blue-grey'];
  return colors[hash % colors.length];
}

function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return hash;
}
