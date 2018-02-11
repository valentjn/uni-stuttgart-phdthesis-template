function generateCitationReference(key)
  reference = ""
  key = key .. ","
  
  for currentKey in key:gmatch("(.-),") do
    author, year = currentKey:match("([A-Za-z]+)([0-9][0-9])")
    currentReference = author:sub(1, 3) .. year
    if reference ~= "" then reference = reference .. "; " end
    reference = reference .. currentReference
  end
  
  tex.print(reference)
end
