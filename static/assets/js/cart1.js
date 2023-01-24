

  // const basket_num  = document.querySelector('#cart_num');
  // const basket_total_price  = document.querySelector('#cart_price');
  
  // let cart_product_number = 0;
  // let total_price = 0;
  // let added_products = { };

  // if(sessionStorage.getItem('cart_product_number') != null){
  //   cart_product_number = Number(sessionStorage.getItem('cart_product_number'));
  //   total_price = Number(sessionStorage.getItem('total_price'));  
  //   basket_num.innerText = cart_product_number;
  //   basket_total_price.innerText = `$${total_price}`;
  // }

  // if(sessionStorage.getItem('added_products') != null){
  //   added_products = sessionStorage.getItem('added_products');
  // }
  
  // function addToCart(product_name, product_image, product_price, product_id){

  //   let product = { 'product_name': product_name, 'product_image': product_image, 'product_price': product_price,'produc_id':product_id}

  //   console.log('Clicked on Add to Cart', product_name, product_image, product_price)
  //   cart_product_number += 1;
  //   total_price += Number(product_price);
  //   console.log("total_price", total_price,typeof(total_price));
  //   sessionStorage.setItem('cart_product_number', cart_product_number);
  //   sessionStorage.setItem('total_price', total_price);

  //   pname = `product${cart_product_number}`;

  //   added_products[pname] = product; 
    
  //   sessionStorage.setItem('added_products', added_products);
  //   // sessionStorage.setItem('product_image', product_image);
  //   // sessionStorage.setItem('product_price', product_price);

  //   basket_num.innerText = cart_product_number;
  //   basket_total_price.innerText = `$${total_price.toFixed()}`;

  // }

//   const basket_num  = document.querySelector('#cart_num');
//   const basket_total_price  = document.querySelector('#cart_price');
  
//   let cart_product_number = 0;
//   let total_price = 0;
//   let added_products = {};

//   if(localStorage.getItem('cart_product_number') != null){
//     cart_product_number = Number(localStorage.getItem('cart_product_number'));
//     total_price = Number(localStorage.getItem('total_price'));  
//     basket_num.innerText = cart_product_number;
//     //total_price = Number(total_price).toFixed(2);
//     basket_total_price.innerText = `$${Number(total_price).toFixed(2)}`;
//   }

//   if(localStorage.getItem('added_products') != null){
//     added_products = localStorage.getItem('added_products');
//     added_products = JSON.parse(added_products); //JSON.parse(JSON.parse(added_products));
//     console.log('added_products', added_products);
//     console.log('added_products keys', Object.keys(added_products));

//   }
  
//   function addToCart(product_name, product_image, product_price, product_id){

//     let product = { 'product_id': product_id, 'product_name': product_name, 'product_image': product_image, 'product_price': product_price, 'product_quantity': 1}

//     console.log('Clicked on Add to Cart', product_name, product_image, product_price)

//     // added_products.forEach(element => {
//     //   console.log(element.product_id, product_id);
//     //   if(element.product_id == product_id){
//     //     element.product_quantity += 1;
//     //   }
//     //   else{
//     //     cart_product_number += 1;
//     //     total_price += Number(product_price);
//     //   }
// // 
//     // });
    
//     cart_product_number += 1;
//     total_price += Number(product_price);
    
//     localStorage.setItem('cart_product_number', cart_product_number);
//     localStorage.setItem('total_price', total_price);

//     // pname = `product${cart_product_number}`;
//     // console.log(pname);
//     console.log('added_products keys', Object.keys(added_products));

//     if(Object.keys(added_products).find(element => element == product_id)){

//       added_products[product_id].product_quantity += 1;
//       console.log('Added Product Quantity', added_products[product_id], added_products[product_id].product_quantity);

//     }
//     else{
//       added_products[product_id] = product; 

//     }
//     //added_products.push(product) ; 

    
//     localStorage.setItem('added_products', JSON.stringify(added_products));

//     // localStorage.setItem('product_image', product_image);
//     // localStorage.setItem('product_price', product_price);

//     basket_num.innerText = cart_product_number;
//     basket_total_price.innerText = `$${total_price}`;
//     console.log('added_products', added_products);

//   }
 

const basket_num  = document.querySelector('#cart_num');
const basket_total_price  = document.querySelector('#cart_price');

let cart_product_number = 0;
let total_price = 0;
let added_products = {};

if(localStorage.getItem('cart_product_number') != null){
  cart_product_number = Number(localStorage.getItem('cart_product_number'));
  total_price = Number(localStorage.getItem('total_price'));  
  basket_num.innerText = cart_product_number;
  //total_price = Number(total_price).toFixed(2);
  basket_total_price.innerText = `$${Number(total_price).toFixed(2)}`;
}

if(localStorage.getItem('added_products') != null){
  added_products = localStorage.getItem('added_products');
  added_products = JSON.parse(added_products); //JSON.parse(JSON.parse(added_products));
  console.log('added_products', added_products);
  console.log('added_products keys', Object.keys(added_products));

}

function addToCart(product_name, product_image, product_price, product_id){

  let product = { 'product_id': product_id, 'product_name': product_name, 'product_image': product_image, 'product_price': product_price, 'product_quantity': 1}

  console.log('Clicked on Add to Cart', product_name, product_image, product_price)


  console.log('added_products keys', Object.keys(added_products));

  if(Object.keys(added_products).find(element => element == product_id)){

    added_products[product_id].product_quantity += 1;
    console.log('Added Product Quantity', added_products[product_id], added_products[product_id].product_quantity);

  }
  else{
    added_products[product_id] = product; 
    cart_product_number += 1;
    localStorage.setItem('cart_product_number', cart_product_number);

  }
  //added_products.push(product) ; 
  total_price += Number(product_price);

  
  localStorage.setItem('total_price', total_price);
  localStorage.setItem('added_products', JSON.stringify(added_products));

  // localStorage.setItem('product_image', product_image);
  // localStorage.setItem('product_price', product_price);

  basket_num.innerText = cart_product_number;
  basket_total_price.innerText = `$${total_price.toFixed(2)}`;
  console.log('added_products', added_products);
  alert('Product Added Successfully');

}


// const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
// 
// const alert = (message, type) => {
//   const wrapper = document.createElement('div')
//   wrapper.innerHTML = [
//     `<div class="alert alert-${type} alert-dismissible" role="alert">`,
//     `   <div>${message}</div>`,
//     '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
//     '</div>'
//   ].join('')
// 
//   alertPlaceholder.append(wrapper)
// }
// 
// const alertTrigger = document.getElementById('liveAlertBtn')
// if (alertTrigger) {
//   alertTrigger.addEventListener('click', () => {
//     alert('Nice, you triggered this alert message!', 'success')
//   })
// }
