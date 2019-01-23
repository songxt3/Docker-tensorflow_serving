$(function() {
    $("#upload_display").click(function() {
        $("#uploadfile").click();
    })
    $("#uploadfile").change(function() {
        $("#form_img").submit();
    })
    $("#upload_background").click(function() {
        $("#uploadfile_left").click();
    })
    $("#uploadfile_left").change(function() {
        $("#left_form_img").submit();
    })
})