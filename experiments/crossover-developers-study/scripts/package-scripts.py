import os
import shutil
import subprocess
#TO EXECUTE IN .vscode IN THE BACKEND



def getOpenAPIAndJar(branch):
  subprocess.run(["git","checkout",branch])
  subprocess.run(["mvn","-f","gen-pom.xml","package"])
  subprocess.run(["cp","./target/todoApp-0.0.1-SNAPSHOT.jar",f"./apps/{branch}.jar"])
  subprocess.run(["cp","../src/main/resources/static/openapi.yml",f"./docs/{branch}.yml"])
  
#making he folders
subprocess.run(["mkdir","./apps"])
subprocess.run(["mkdir","./docs"])
subprocess.run(["mkdir","./apps/set1"])
subprocess.run(["mkdir","./docs/set1"])
subprocess.run(["mkdir","./apps/set2"])
subprocess.run(["mkdir","./docs/set2"])

getOpenAPIAndJar("experiment-start")
for i in range(1,3):
  for j in range(1,6):
    getOpenAPIAndJar(f"set{i}/evo{j}")

