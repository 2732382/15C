function filterGroups() {
    var input, filter, div, a, i, txtValue;
    input = document.getElementById('groupSearch');
    filter = input.value.toUpperCase();
    div = document.getElementById('groupList');
    a = div.getElementsByTagName('a');
    for (i = 0; i < a.length; i++) {
        txtValue = a[i].textContent || a[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}