using System.Collections.Generic;
using System.Linq;

namespace iothubsigfox
{
    public static class ExtBase
    {
        public static IEnumerable<string> ChunkString(this string val, int chunkSize)
        {
            return val.Select((x, i) => new { Index = i, Value = x })
                      .GroupBy(x => x.Index / chunkSize, x => x.Value)
                      .Select(x => string.Join("", x));
        }
    }
}