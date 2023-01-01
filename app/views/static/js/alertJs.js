const alertButton=document.querySelector(".btn-close")
const divAlert=document.querySelector(".alert")

alertButton.addEventListener("click",()=>{
    divAlert.remove();
});