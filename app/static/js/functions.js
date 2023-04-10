

function updateOptions($select, $query_type_val, $query_term_val) {
    $.ajax({
        url: "/search_term/",
        type: 'GET',
        data: {
            search : $query_term_val,
            type : 'public',
            query_type : $query_type_val
        },
        success: function(res) {
            $select.empty();
            for (option in res) {
                $option = `<option value='${res[option].text}' id='option-term-${option}'>`;
                $select.append($option)
            }
        }
    });
}


function appendSearch() {
    $.ajax({
        url: '/get_search_term',
        type:'GET',
        success: function(data) {
            let $data = $(data);
            let search_col_no = $('.search-query').length + 1
            $data.attr('id',`search-col-${search_col_no}`);
            $data.find('.query-term').attr('list',`query-term-list-${search_col_no}`);
            let $select = $data.find('.query-term-list');
            $select.attr('id',`query-term-list-${search_col_no}`)
        $('.search-terms').append($data);
        if (search_col_no == 1) {
            $('.remove-btn').remove();
        }
        $(".remove-btn").each(function() {
            $(this).on('click', function(e) {
                e.preventDefault();
                $(this).parent().remove();
            }) 
        })
        let $query_type = $data.find(".query-type");
        let $query_term = $data.find(".query-term");
        let $query_type_val = $query_type.val();
        let $query_term_val = $query_term.val();
        updateOptions($select, $query_type_val, $query_term_val);
        $query_type.on('change', function() {
            let $query_type_val = $query_type.val();
            let $query_term_val = $query_term.val();
            updateOptions($select, $query_type_val, $query_term_val);
        });
        $query_term.on('keyup', function() {
            let $query_type_val = $query_type.val();
            let $query_term_val = $query_term.val();
            updateOptions($select, $query_type_val, $query_term_val);
        })
    }             
    })
}
