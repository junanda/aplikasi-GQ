$("#btnCalculate").on("click",function(){

    let data = JSON.stringify({
        'data': {
            'nilai_skp': $("#nilai_skp").val(),
            'nilai_orientasi': $("#nilai_orientasi").val(),
            'nilai_integritas': $("#nilai_integritas").val(),
            'nilai_komitmen': $("#nilai_komitmen").val(),
            'nilai_disiplin': $("#nilai_disiplin").val(),
            'nilai_kerjasama': $("#nilai_kerjasama").val(),
            'nilai_k': $("#nilai_k").val()
        },
        'nama': $("#nama_pegawai").val()
    })

    var html = '<table class="table table-striped table-border"><thead><tr><th>Result</th><th></th></tr></thead>';

    html += '<tbody>';

    $.ajax({
        type: "POST",
        url: `${urlbase}calculate`,
        dataType: 'json',
        data: data,
        contentType: 'application/json',
        processData: false,
        success: function(res){
            var datar = res.data;
            
            html += `<tr><td>Nama </td><td>${datar.nama}</td></tr>`;
            html += `<tr><td>Jumlah Ketetanggaan</td><td>${datar.jumlah_ketetanggaan}</td></tr>`;
            html += `<tr><td>Jarak Maksimum</td><td>${datar.jarak_maksimum}</td></tr>`;
            html += `<tr><td>Jarak Minimum</td><td>${datar.jarak_minimum}</td></tr>`;
            html += `<tr><td>Label</td><td>${datar.label}</td></tr>`;
            html += '</tbody></table>';
            $("#result").html(html);
        }
    });

})