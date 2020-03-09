/* Project specific Javascript goes here. */
$(document).ready(function() {
    $('#datatable').DataTable({
        ordering: true,
        searching: true,
        dom: 'B<"clear">lfrtip',
        buttons: true
    });
} );
