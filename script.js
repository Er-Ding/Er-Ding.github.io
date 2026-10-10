const tabs = document.querySelectorAll(".filter-tabs [data-filter]");
const items = document.querySelectorAll(".work-item");
const filters = new Set([...tabs].map((tab) => tab.dataset.filter));

console.assert(
  [...items].every((item) => filters.has(item.dataset.type)),
  "每条成果的 data-type 必须与筛选按钮的 data-filter 对应。",
);

for (const tab of tabs) {
  tab.addEventListener("click", () => {
    for (const button of tabs) {
      button.classList.toggle("active", button === tab);
      button.setAttribute("aria-selected", button === tab);
    }
    for (const item of items) {
      item.hidden = tab.dataset.filter !== "全部" && item.dataset.type !== tab.dataset.filter;
    }
  });
}
