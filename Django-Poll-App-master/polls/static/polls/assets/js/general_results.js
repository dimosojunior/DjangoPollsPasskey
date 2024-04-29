
  $(document).ready(function(){
    $('#div_id_physics').hide()
    $('#more-line').click(function(){
        $('#div_id_physics').slideToggle(200)
        

    });

    $('#id_physics, #id_chemistry, #id_biology, #id_civics, #id_history, #id_english, #id_kiswahili, #id_mathematics, #id_geography').keyup(function(){
        
        var physics_text = $('#id_physics').val();

        

        var chemistry_text = $('#id_chemistry').val();
        

        var biology_text = $('#id_biology').val();
        

        var civics_text = $('#id_civics').val();
        

        var history_text = $('#id_history').val();


        var english_text = $('#id_english').val();

        var kiswahili_text = $('#id_kiswahili').val();

        var mathematics_text = $('#id_mathematics').val();
        

        var geography_text = $('#id_geography').val();

        
        var total_marks = (physics_text * 1)  + (chemistry_text * 1) + (biology_text * 1) + (civics_text * 1) + (history_text * 1) + (english_text * 1) + (kiswahili_text * 1) + (mathematics_text * 1) + (geography_text * 1)
    
    
        var average = total_marks / 9
    
        $('#id_student_total').val(total_marks);
        
        $('#id_student_average').val(average);
    });

});








    