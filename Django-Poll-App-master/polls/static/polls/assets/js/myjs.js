
  $(document).ready(function(){
    $('#div_id_Test5').hide()
    $('#more-line').click(function(){
        $('#div_id_Test5').slideToggle(200)
        

    });

    $('#id_Test1, #id_Test2, #id_Test3, #id_Test4, #id_Test5, #id_MidTerm, #id_Term').keyup(function(){
        var Test1_text = $('#id_Test1').val();

        

        var Test2_text = $('#id_Test2').val();
        

        var Test3_text = $('#id_Test3').val();
        

        var Test4_text = $('#id_Test4').val();
        

        var Test5_text = $('#id_Test5').val();


        var MidTerm_text = $('#id_MidTerm').val();

        var Term_text = $('#id_Term').val();
        
        
        var all_total = (Test1_text * 1)  + (Test2_text * 1) + (Test3_text * 1) + (Test4_text * 1) + (Test5_text * 1) + (MidTerm_text * 1) + (Term_text * 1)
    
    
        var average = all_total / 7
    
        $('#id_total_marks').val(all_total);
        
        $('#id_Average').val(average);
    });

});








    