/**
*  Converts a number to Scientific Notation
* Use for example as:
* <script language="javascript"> document.write(to_scientific_notation({{ run.protonCharge }})); </script>
*/
function to_scientific_notation(num, decimals) {
    if (typeof(decimals)==='undefined') decimals = 2;
    try {
        var ret = num.toExponential(decimals);
        return ret;
    } catch (e) {
        return num;
    }
};
