document.onreadystatechange = subSomething;
function subSomething() {
    if (document.readyState == "complete") {
        $('#loading').delay(800).hide(0);
        $('#show_part').delay(800).show(0);
        $('.loader').delay(800).fadeOut('slow');
    }
}