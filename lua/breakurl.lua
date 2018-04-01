-- https://yingtongli.me/blog/2016/01/08/breaking-urls-anywhere-in-lualatex-even.html
function breakurl(url, label)
  oldLabel = label;
  
  if string.sub(label, 1, 12) == "\\nolinkurl {" then
    label = string.sub(label, 13, string.len(label) - 1)
  end
  
  -- label = label:gsub(".", "%1\\allowbreak{}")
  label = label:gsub(".", "%1\\penalty 100 ")
  
  label = label:gsub("~", "\\textasciitilde")
  label = label:gsub("&", "\\&")
  label = label:gsub("_", "\\_")
  
  -- insert other URL symbols here
  
  if oldLabel == url then
    tex.print("\\oldhref{" .. url .. "}{\\texttt{" .. label .. "}}")
  else
    tex.print("\\oldhref{" .. url .. "}{" .. oldLabel .. "}")
  end
end
