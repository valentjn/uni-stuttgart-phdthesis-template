function execute(command)
  local i, j = io.popen(command)
  if not i then
    print(j)
    os.exit(-1)
  end
  local output = i:read("*all")
  i:close()
  return output
end

function executePrint(command)
  tex.print(execute(command))
end

function getGitCommitHash()
  local gitHash = execute("git log -1 --pretty=format:%h")
  local gitStatus = execute("git status --porcelain")
  local n = 0
  for i in gitStatus:gmatch("\n") do n = n + 1 end
  if n > 1 then
    gitHash = gitHash .. "*"
  end
  tex.print(gitHash)
end

function getGitCommitTimeShort()
  executePrint("LC_ALL=en_US git log -1 --pretty=format:%cd '--date=format:%b %d, %l:%M%P'")
end

function getGitCommitTimeLong()
  executePrint("LC_ALL=en_US git log -1 --pretty=format:%cd '--date=format:%B %e, %Y at %l:%M%P'")
end

function getCurrentTimeShort()
  executePrint("LC_ALL=en_US date '+%b %d, %l:%M%P' | tr -d '\n'")
end

function getCurrentTimeLong()
  executePrint("LC_ALL=en_US date '+%B %e, %Y at %l:%M%P' | tr -d '\n'")
end

function getAndIncreaseCompileCounter()
  path = "../../compileCounter.txt"
  
  f = io.open(path, "r")
  local counter = f:read("*n")
  f:close()
  
  counter = tostring(counter + 1)
  
  f = io.open(path, "w+")
  f:write(counter .. "\n")
  f:close()
  
  tex.print(counter)
end
