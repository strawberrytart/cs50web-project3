$(document).ready(function () {

    
    $('.regular, .sicilian').on('click', function(){
        add_pizza($(this))
    });

    $('.subs, .pasta, .platter, .salads').on('click', function(){
        add_subs($(this))
    });

    $('.place-order').on('click', function(){
        ToggleModal();
    });

    $('#add-to-cart').on('click', function(e){
        e.preventDefault();
        var message=[];
        var flag_pizza=true;
        if ($(this).data('name')=='subs'){
            $("input[type=checkbox]:checked").each(function(){
                message.push($(this).attr('id'));
            })
            flag_pizza=false;
        }
        else if($(this).data('name')=='pizza'){
            $('.topping-dropdown option:selected').each(function(){
                message.push($(this).text());
            })
        };
        message= message.join(', ')
        $.ajax({
            type:'post',
            url:'add_to_cart',
            dataType: "json",
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                message:message,
                dish:$('.popup-title > h3').text(),
                price:$('#price').text(),
                flag:flag_pizza
            },
            success:function(response){
                $('.modall-content').removeClass('active');
                $('.modall').removeClass('show-modall');
                alert('Added '+ response.dish)
            }
        });
    });

    $('.modall').on('click', function(){
        $('.modall-content').removeClass('active');
        $('.modall').removeClass('show-modall');
    });

    $('.delete').on('click', function(){
        delete_cart($(this))
    });

    $('button:contains("Back")').on('click',function(){
        $('.modall-content').removeClass('active');
        $('.modall').removeClass('show-modall');
    });

    $(".accordion_header").click(function(){
        $(".accordion_header").removeClass("active");
       $(this).addClass("active");
    });
});


function delete_cart(element){
    name=element.data('id');
    $.ajax({
        url:'delete_cart',
        type:'post',
        dataType: "json",
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            id:name
        },
        success:function(){
           location.reload(true);
        }
    });
};




function add_pizza(element){
    name= element.data('name');
    size= element.data('size');
    price= element.data('price');
    $.ajax({
        url:'modal',
        type: 'get',
        async:true,
        dataType:"json",
        data:{name: name, button_class: element.attr('class')
        },
        success:function(response){
            $('.toppings-selection').empty();
            $('.popup-title').empty();
            if (element.attr('class')=="regular"){
                $('.popup-title').append((`<h3>${size} Regular ${name} Pizza </h3>`))
                $('.popup-title').append($(`<h6 id='price'> ${price}</h6>`))
            }
            else{
                $('.popup-title').append((`<h3>${size} Sicilian ${name} Pizza </h3>`))
                $('.popup-title').append($(`<h6 id='price'> ${price}</h6>`))
            }
            $('#add-to-cart').attr('data-name','pizza')
            for (var i=0; i< response.n; i++){
                console.log(i)
                var options=$(`<select class="topping-dropdown"></select>`);
                for (var j=0; j< response.toppings.length; j++){
                    topping=response.toppings[j];
                    console.log(topping)
                    options.append(`<option value="${topping.id}">${topping.name}</option>`);
                };
                $('.toppings-selection').append(options)
            };
            ToggleModal();
        }
    }); 
};

function ToggleModal(){
    $('.modall').toggleClass('show-modall');
    $('.modall-content').addClass('active');
};

function add_subs(element){
    name= element.data('name');
    size= element.data('size');
    if (size == undefined){
        size=""
    }
    price= element.data('price');
    $.ajax({
        url:'modal_other',
        type: 'get',
        async:true,
        dataType:"json",
        data:{name: name, button_class: element.attr('class')
        },
        success:function(response){
            $('.toppings-selection').empty();
            $('.popup-title').empty();
            /*$('.toppings-selection').next('h6').remove();*/
            $('#add-to-cart').removeAttr('data-name');
            console.log(price);
            console.log(size);
            if (element.attr('class')=='subs'){
                $('.popup-title').append((`<h3>${size} ${name} Sub</h3>`))
                $('.popup-title').append($(`<h6 id='price_before'> ${price}</h6>`))
                $('#add-to-cart').attr('data-name','subs')
            }
            else if (element.attr('class')=='platter'){
                $('.popup-title').append((`<h3>${size} ${name} Dinner Platter</h3>`))
                $('.popup-title').append($(`<h6 id='price'> ${price}</h6>`))
            }
            else{
                $('.popup-title').append((`<h3>${size} ${name}</h3>`))
                $('.popup-title').append($(`<h6 id='price'> ${price}</h6>`))
            }
            for (var j=0; j< response.obj.length; j++){
                div=$('<div class="form-check"> </div>')
                extra=response.obj[j];
                input=$(`<input class="form-check-input" type="checkbox" value= "${extra.price}" id="${extra.name}">`)
                label=$(`<label class="form-check-label" for= "${extra.name}" > ${extra.name} - ${extra.price}</label>`)
                div.append(input)
                div.append(label)
                $('.toppings-selection').append(div)
            };
            if (element.attr('class')=='subs'){
                $('.toppings-selection').append($(`<h6> Total: <span id='price'>${price} <span></h6>`))
            }
            ToggleModal();
        }
    }); 
}

function CalculateTotal(){
    var total=parseFloat($('#price_before').html()) /*convert text to float to 2 decimal places*/ 
    console.log(total)
    $('input[type=checkbox]:checked').each(function(){
        total+=parseFloat($(this).val());
    });
    console.log(total)
    $('#price').html(total);
}

$(document).on('change', "input[type=checkbox]",function(){
    CalculateTotal();
})


