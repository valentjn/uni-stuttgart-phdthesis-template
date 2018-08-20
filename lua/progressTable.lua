function generateTotalRow()
  progressTexPath = "../../tex/document/progress.tex"
  sum = {}
  nRows = 0
  
  for i = 0, 18 do
    sum[i] = 0
  end
  
  for line in io.lines(progressTexPath) do
    local _, nSeparators = line:gsub("&", "")
    
    if nSeparators == 13 then
      nRows = nRows + 1
      line = line:gsub("\\thead", "")
      i = 0
      
      for s in line:gmatch("[^&]+") do
        if (i ~= 0) and (i ~= 3) and (i ~= 6) and (i ~= 13) then
          weighted = false
          ignore = false
          
          if i == 12 then
            s = s:gsub("\\\\.*", ""):gsub("\\tfoot", "")
            s = s:gsub("\\pr{", ""):gsub("}", "")
            weighted = true
          elseif (i >= 7) and (i <= 11) then
            if s:find("%-%-") then
              ignore = true
            else
              s = s:gsub("\\yes", "1"):gsub("\\no", "0")
              weighted = true
              sum[i+7] = sum[i+7] + pageCount
            end
          end
          
          if not ignore then
            summand = tonumber(s)
            
            if i == 2 then
              pageCount = summand
            end
            
            if weighted then
              summand = pageCount * summand
            end
            
            sum[i] = sum[i] + summand
          end
        end
        
        i = i + 1
      end
    end
  end
  
  output = string.format([[
\\ \midrule
$\sum$ &
%u & %u & \pr{%.0f} &
%u & %u & \pr{%.0f} &
\pc{%.0f} & \pc{%.0f} & \pc{%.0f} &
\pc{%.0f} & \pc{%.0f} &
\pr{%.0f}]],
      sum[1], sum[2], 100*sum[1]/sum[2],
      sum[4], sum[5], 100*sum[4]/sum[5],
      100*sum[7] /sum[14], 100*sum[8] /sum[15], 100*sum[9] /sum[16],
      100*sum[10]/sum[17], 100*sum[11]/sum[18],
      sum[12]/sum[2])
  output = output:gsub("\n", " ")
  
  tex.print(output)
end
