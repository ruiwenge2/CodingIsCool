languages = {
  "HTML":"html",
  "CSS":"css",
  "JavaScript":"js",
  "Python":"py",
  "Java":"java",
  "C":"c",
  "C++":"cpp",
  "C#":"cs",
  "JSON":"json",
  "SVG":"svg",
  "CSV":"csv",
  "Plain Text":"txt"
}

modes = {
  "html":"html",
  "css":"css",
  "js":"javascript",
  "py":"python",
  "java":"java",
  "c":"c_cpp",
  "cpp":"c_cpp",
  "cs":"csharp",
  "json":"json",
  "svg":"html",
  "csv":"text",
  "txt":"text"
}

filetypes = {
  "html":"text/html",
  "css":"text/css",
  "js":"text/javascript",
  "py":"text/x-python-script",
  "java":"text/plain",
  "c":"text/plain",
  "cpp":"text/plain",
  "cs":"text/plain",
  "json":"application/json",
  "svg":"image/svg+xml",
  "csv":"text/csv",
  "txt":"text/plain"
}

filestarts = {
  "html":"""<!DOCTYPE html>
<html>
	<head></head>
	<body></body>
</html>""",
  "css":"""body {
}""",
  "js":"",
  "py":"",
  "java":"""public class FILENAME {
	public static void main(String[] args) {
		System.out.println("Hello World!");
	}
}""",
  "c":"""#include <stdio.h>

int main(void) {
  printf("Hello World");
  return 0;
}""",
  "cpp":"""#include <iostream>

int main() {
  std::cout << "Hello World!";
}""",
  "cs":"""using System;

class MainClass {
  public static void Main (string[] args) {
    Console.WriteLine ("Hello World");
  }
}""",
  "json":"{}",
  "svg":"""<svg version="1.1" xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" xml:space="preserve"></svg>""",
  "csv":"",
  "txt":""
}