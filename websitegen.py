import os
import easygui

script = input("Enter the name of the script > ")
message = input("Enter a brief description of the script > ")
teaser = input("Enter an even briefer description of the script > ")

print("Pick the index.html file from the website.")
browser = easygui.fileopenbox(msg="Pick the index.html file from the website.")

tableElement = f"""													<tr>
														<td>{script}</td>
														<td>{teaser}</td>
														<td style="text-align:right"><a href="{script}.html#downloads" class="button primary">Go to Downloads</a></td>
													</tr>\n"""

template = f"""<!DOCTYPE HTML>
<!--
	Stellar by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>{script} - Mash</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Header -->
				<header id="header" class="alt">
					<span class="logo"><img src="https://raw.githubusercontent.com/ModMonster/mish/master/logo.png" alt="" /></span>
					<h1>Mash Command Database</h1>
				</header>

				<!-- Nav -->
					<nav id="nav">
						<ul>
							<li><a href="#info" class="active">Information</a></li>
							<li><a href="#downloads">Download</a></li>
							<li><a href="#get-started">Get Started</a></li>
						</ul>
					</nav>

				<!-- Main -->
					<div id="main">

						<!-- Introduction -->
							<section id="info" class="main">
								<div class="spotlight">
									<div class="content">
										<header class="major">
											<h2>{script}</h2>
											<p>{message}</p>
										</header>
									</div>
								</div>
							</section>

						<!-- Downloads -->
							<section id="downloads" class="main special">
								<header class="major">
									<h2>Download</h2>
								</header>
								<ul class="features">
									<li>
										<span class="icon solid major style1 fa-code"></span>
										<h3>Download through Mash</h3>
										<h6 style="color: green; line-height: 0px;">Recommended</h6>
										<br>
										<p>To install this command on a supported Mish install, simply run</p>
										<code style="line-height: 0px;">mash install {script}</code>
									</li>
									<li>
										<span class="icon major style3 fa-copy"></span>
										<h3>Manual Download</h3>
										<h6 style="color: green; line-height: 0px;">­</h6>
										<br>
										<p>You can also download the files for manual installation.</p>
										<a href="https://modmonster.github.io/mash/{script}/{script}.py" class="button icon solid fa-download">Download</a>
									</li>
								</ul>
							</section>

						<!-- Get Started -->
							<section id="get-started" class="main special">
								<header class="major">
									<h2>Download Mish</h2>
									<p>Mod's Interactive Shell, aka Mish is a simple shell made in Python.</p>
								</header>
								<footer class="major">
									<ul class="actions special">
										<li><a href="https://github.com/modmonster/mish/releases/" class="button primary">Download</a></li>
										<li><a href="https://github.com/modmonster/mish" class="button">View on GitHub</a></li>
									</ul>
								</footer>
							</section>

					</div>

				<!-- Footer -->
					<footer>
						<p align="center" class="copyright">&copy; ModMonster 2021. Design: <a href="https://html5up.net">HTML5 UP</a>.</p>
					</footer>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>"""

print("Select a location to save HTML file")
savePath = easygui.filesavebox(msg="Select a location to save HTML file", default=script + ".html")

if (savePath != None):
    file = open(savePath, "w", encoding="utf-8")
    file.write(template)
    file.close()

if (browser != None):
	file = open(browser, "r")
	contents = file.readlines()
	file.close()
	endLine = contents.index("												</tbody>\n")
	contents.insert(endLine, tableElement)
	print(contents)
	file = open(browser, "w")
	file.writelines(contents)
	file.close()