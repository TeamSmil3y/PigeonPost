function count() {
    let counter = Number(document.getElementById('counter').innerHTML)
    window.location.replace(location.pathname+'?counter='+(counter+1))
}