// Concept-only storefront behavior for lionel.html: size choice and a local cart counter.
const $=selector=>document.querySelector(selector);
const add=$('#add-to-cart'),count=$('#cart-count'),cart=$('#cart-button');
let items=0,timer;
document.querySelectorAll('.sizes [role=radio]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.sizes [role=radio]').forEach(other=>other.setAttribute('aria-checked',String(other===button)));
}));
add?.addEventListener('click',()=>{
  items+=1;count.textContent=String(items);
  const label=add.dataset.label||(add.dataset.label=add.textContent);
  add.textContent=add.dataset.done;add.classList.add('done');cart.classList.add('bump');
  clearTimeout(timer);timer=setTimeout(()=>{add.textContent=label;add.classList.remove('done');cart.classList.remove('bump');},1400);
});
