$(document).ready(function() {
    $('#like_btn').click(function(){
        var categoryIdVar;
        categoryIdVar = $(this).attr("data-categoryid");
        articleIdVar = $(this).attr("data-articleid");

        $.get('/rango/like_category/', {category_id: categoryIdVar}, function(data){
            $('#like_count').html(data);
            $('#like_btn').hide();
        });

        $.get('/rango/like_article/', {article_id: articleIdVar}, function(data){
            $('#like_count').html(data);
            $('#like_btn').hide();
        });
    });

    $('#search-input').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/rango/suggest/', {'suggestion': query}, function(data){
            $('#categories-listing').html(data);
        });
    });
});