
function initViz() {
    var containerDiv = document.getElementById("vizContainer-1"),
    // url = "https://public.tableau.com/profile/reshmi5500#!/vizhome/CreditCard0/Dashboard1";

    // url = "https://public.tableau.com/views/CreditCard0/creditcardstory";
     url = "https://public.tableau.com/views/CreditCard-1/creditcardstory";

    // url = "https://public.tableau.com/views/CreditCard-1/Dash_Age";
    


    var viz = new tableau.Viz(containerDiv, url);
}

initViz();