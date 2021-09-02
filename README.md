# ChromebookCheckoutTool
This script will compile the needed chrome cart data into csv files for MG Campus
The Python version of the scripts require >= python3

<h2><b>20210902 NOTE</h2></b>
I have commented out the conversion of the autoUpdateExpiration date into human readable format as it is no longer needed in my environment.</br>  If your AUE dates are still not being pulled in from GAM already in human readable format, please uncomment the following:</br>
/scripts/deprovisioned_unit.py, lines 37-39</br>
/scripts/cart_script.py, lines 60-62</br>

<h2><b>NOTES: </b></h2>This script requires other files generated by <a href="https://github.com/jay0lee/GAM">GAM</a> (thanks to <a href="https://github.com/jay0lee">jay0lee</a>) that are not provided in this repository.</br></br>

Thank You to <a href="https://github.com/unixabg"/>Richard Nelson - unixabg</a> for your help with the date and substr portion of the awk call in this script.</br></br>

--I will be adding more sanity checks and error checking later. </br>
--I will be adding example code for creating data csv files using GAM. (Will not go into installing GAM as they can be found using link above)</br></br>

<h3>CVS DATA NOTES</h3>
The following command will help to find the column number of your desired header field:

$<code>sed -n $'1s/,/\\\n/gp' &lt;FILENAME OF CSV FILE TO SEARCH&gt; | grep -nx &lt;WANTED FIELD&gt; </code></br></br>

<h3><b>Using Tool</b></h3></br>
This tool was designed specifically for use on the MG Campus in order to gather data using GAM, then upload the data into <a href="https://github.com/snipe/snipe-it"/>Snipe-IT - Github</a>  or <a href="https://snipeitapp.com/"</a>Snipe-IT - Website</a> with the end goal of a checkout system. This means that the directory names, script variables, and created filenames are specific for the MG OU structure.</br>
