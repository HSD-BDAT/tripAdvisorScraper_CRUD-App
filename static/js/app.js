$(function() {
    //If check_all checked then check all table rows
    $("#check_all").on("click", function() {
        if ($("input:checkbox").prop("checked")) {
            $("input:checkbox[name='row-check']").prop("checked", true);
        } else {
            $("input:checkbox[name='row-check']").prop("checked", false);
        }
    });

    // Check each table row checkbox
    $("input:checkbox[name='row-check']").on("change", function() {
        var total_check_boxes = $("input:checkbox[name='row-check']").length;
        var total_checked_boxes = $("input:checkbox[name='row-check']:checked").length;

        // If all checked manually then check check_all checkbox
        if (total_check_boxes === total_checked_boxes) {
            $("#check_all").prop("checked", true);
        } else {
            $("#check_all").prop("checked", false);
        }
    });

    $("#delete_selected").on("click", function() {
        var ids = '';
        var comma = '';
        // delete the rows with the checkbox checked
        $("input:checkbox[name='row-check']:checked").each(function() {
            ids = ids + comma + this.value;
            comma = ',';
        });

        if (ids.length > 0) {
            $.ajax({
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                url: "http://localhost:5000/delete_products",
                data: JSON.stringify({ 'ids': ids }),
                dataType: "json",
                cache: false,
                success: function(msg) {
                    $("#msg").html(msg);
                },
            });
        } else {
            $("#msg").html('<span style="color:red;">You must select at least one product for deletion</span>');
        }
    });

    $("#edit").on("click", function() {
        var ids = '';
        var comma = '';
        $("input:checkbox[name='row-check']:checked").each(function() {
            ids = ids + comma + this.value;
            comma = ',';
        });

        if (ids.length > 0) {
            $.ajax({
                type: "POST",
                contentType: 'application/json;charset=UTF-8',
                url: "http://localhost:5000/edit",
                data: JSON.stringify({ 'ids': ids }),
                dataType: "json",
                cache: false,
                success: function(msg) {
                    $("#msg").html(msg);
                },
            });
        } else {
            $("#msg").html('<span style="color:red;">You must select at least one product for deletion</span>');
        }
    });
});