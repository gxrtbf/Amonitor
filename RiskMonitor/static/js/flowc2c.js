$(document).ready(function(){

    var cdata = {
        'table': "flowc2c",
        'content': "item"
    };
    $.ajax({
        type: 'POST',
        url: "../api/v1/day/?format=json",
        data: {
            para: JSON.stringify(cdata),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
        },
        success: function(dataset){
            console.log(dataset)
            $('#tdata').DataTable( {
                data: dataset,
                columns: [
                    { data: 'member' },
                    { data: 'loanCount' },
                    { data: 'loanMoney' },
                    { data: 'loanCountTerm' },
                    { data: 'loanCountTermNo' },
                    { data: 'delayRate0' },
                    { data: 'allCountTerm' },
                    { data: 'CountTerm7' },
                    { data: 'delayRate7' }
                ]
            } );
        }
    });
});