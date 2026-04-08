function buttonOnClick(test, IdSender, T_Event) {
    console.log(test);
    console.log(T_Event);
    console.log(IdSender);

    e = document.getElementById(this.id);
    e.textContent = "click";
}