String::splice = (idx, rem, s) ->
  @slice(0, idx) + s + @slice(idx + Math.abs(rem))

String::linkForPositions = (positions) ->
  offset = 0
  out = @
  for p in positions
    out = out.splice p.location + offset, 0, '['
    offset += 2
    console.log offset
    out = out.splice p.location + offset + p.length, 0, ']'
    console.log offset
  out