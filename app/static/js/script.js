$(function() {
    const d = new Date();
    let year = d.getFullYear();
    $('#date').text(year);
    appendSearch();
    $('.view_table').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('th.sorting').each(function() {
        $(this).text($(this).text()
            .replace("$","")
            .replaceAll("_"," "))
            .css('textTransform', 'capitalize');
    });
    let form_submit = $('#search-form').on('submit', function(e) {  
        $(".search-query").each(function() {
            $this = $(this);
            $query_term = $(this).find(".query-term");
            $query_type = $(this).find(".query-type");
            if ($query_term.val() != '') {
                $("<input>").attr({
                    'type':'hidden',
                    'name': $this.attr("id") + "-query-term"
                }).val($query_term.val()).appendTo(form_submit);
                $("<input>").attr({
                    'type':'hidden',
                    'name': $this.attr("id") + "-query-type"
                }).val($query_type.val()).appendTo(form_submit);
            }
        })
    });
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
    });
    $("#add-btn-btn").on("click", function(e) {
        if ($('.search-query').length <= 3) {
            appendSearch();
        }
        else {
            e.preventDefault();
        }
    })
    $('td').each(function() {
        var content = $(this).html();
        content = content.replace(/\\n/g, '<br>');
        content = content.replace('NaN', '-')
        content = content.replace(/\n/g, '<br>')
        $(this).html(content);
        if (($(this).height() / $(this).width()) > 3) {
            $(this).css('width',$(this).height());
        }
    })
})