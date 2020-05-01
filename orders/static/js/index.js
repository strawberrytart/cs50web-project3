$(document).ready(function () {

    /*
    $(".reg-pizza").on('click', function(){
        $('.modall').toggleClass('show-modall');
        $('.modall-content').addClass('active');
    });
    */
   /*
     $('.reg-pizza').click(function(){
        $.ajax({
            url:'modal',
            type: 'get',
            async:true,
            dataType:"json",
            data:{ csrfmiddlewaretoken: '{{ csrf_token }}', button_text: $(this).text()
            },
            success:function(response){
                var options=$(".topping-dropdown");
                for (var i=0; i<response.toppings.length; i++){
                    topping=response.toppings[i];
                    options.append(`<option value="${topping.id}"> ${topping.name} </option>`);
                };
                ToggleModal();
            }
        });   
    });
    */


    $('#add-to-cart').on('click', function(e){
        e.preventDefault();
        $.ajax({
            type:'post',
            url:'add_to_cart',
            dataType: "json",
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                toppings_0:$('#topping-dropdown-0 :selected').text(),
                toppings_1:$('#topping-dropdown-1 :selected').text(),
                toppings_2:$('#topping-dropdown-2 :selected').text(),
            },
            success:function(response){
                $('.modall-content').removeClass('active');
                $('.modall').removeClass('show-modall');
                alert(response.obj)
            }
        });
    });

    $('.modall').on('click', function(){
        $('.modall-content').removeClass('active');
        $('.modall').removeClass('show-modall');
    });
});

function add_pizza(name,size,price,obj){
    $.ajax({
        url:'modal',
        type: 'get',
        async:true,
        dataType:"json",
        data:{name: name, button_class: $(obj).attr('class')
        },
        success:function(response){
            $('.toppings-selection').empty();
            $('.toppings-selection').append((`<h3> ${name}-${size}-${price}</h3>`))
            for (var i=0; i< response.n; i++){
                console.log(i)
                var options=$(`<select id="topping-dropdown-${i}"></select>`);
                for (var j=0; j< response.toppings.length; j++){
                    topping=response.toppings[j];
                    console.log(topping)
                    options.append(`<option value="${topping.id}"> ${topping.name} </option>`);
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

function add_subs(name,price,size="", obj=""){
    $.ajax({
        url:'modal_other',
        type: 'get',
        async:true,
        dataType:"json",
        data:{name: name, button_class:$(obj).attr('class')
        },
        success:function(response){
            $('.toppings-selection').empty();
            console.log(price)
            console.log(size)
            $('.toppings-selection').append((`<h3>${size} ${name} ${price}</h3>`))
            for (var j=0; j< response.obj.length; j++){
                div=$('<div class="form-check"> </div>')
                extra=response.obj[j];
                input=$(`<input class="form-check-input" type="checkbox" value=${extra.name} id=${extra.name} >`)
                label=$(`<label class="form-check-label" for=${extra.name} >${extra.name} - $${extra.price}</label>`)
                div.append(input)
                div.append(label)
                $('.toppings-selection').append(div)
            };
            ToggleModal();
        }
    }); 
}



