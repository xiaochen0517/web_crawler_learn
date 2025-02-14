import {parse} from "@babel/parser";
import generate from "@babel/generator";
import fs from "fs";
import {traverse} from "@babel/core";

const code = fs.readFileSync("code/code1.js", "utf-8");
let ast = parse(code);

traverse(ast, {
  CallExpression(path) {
    let node = path.node;
    if (node.callee.object.name === "console" && node.callee.property.name === "log") {
      path.remove();
    }
  }
});

const {code: generatedCode} = generate(ast);
console.log(generatedCode);
