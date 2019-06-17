document.onreadystatechange = subSomething;
function subSomething() {
    if (document.readyState == "complete") {
        $('#loading').delay(1300).hide(0);
        $('#show_area').delay(1300).show(0);
        $('#info_area').delay(1300).show(0);
        $('.loader').delay(1300).fadeOut('slow');
    }
}