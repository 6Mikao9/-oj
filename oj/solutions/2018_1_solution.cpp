#include <bits/stdc++.h>
using namespace std;

struct Segment {
    int sx, sy, ex, ey;
    int count;
};

map<pair<int,int>, Segment*> startMap;
map<pair<int,int>, Segment*> endMap;

int main() {
    int n;
    cin >> n;
    
    vector<Segment> segs(n);
    int maxCount = 0, maxX = 0, maxY = 0;
    
    for (int i = 0; i < n; i++) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        
        segs[i] = {x1, y1, x2, y2, 1};
        
        // 检查是否可以和前面的线段连接
        pair<int,int> start = {x1, y1};
        pair<int,int> end = {x2, y2};
        
        // 查找以当前起点为终点的线段（前面有线段的终点是当前起点）
        Segment* prevSeg = nullptr;
        if (endMap.count(start)) {
            prevSeg = endMap[start];
        }
        
        // 查找以当前终点为起点的线段（后面有线段的起点是当前终点）
        Segment* nextSeg = nullptr;
        if (startMap.count(end)) {
            nextSeg = startMap[end];
        }
        
        if (prevSeg && nextSeg) {
            // 同时连接前后两段
            segs[i].sx = prevSeg->sx;
            segs[i].sy = prevSeg->sy;
            segs[i].ex = nextSeg->ex;
            segs[i].ey = nextSeg->ey;
            segs[i].count = prevSeg->count + 1 + nextSeg->count;
            
            // 更新被合并线段的信息（它们不再作为独立线段存在）
            startMap.erase({prevSeg->sx, prevSeg->sy});
            endMap.erase({prevSeg->ex, prevSeg->ey});
            startMap.erase({nextSeg->sx, nextSeg->sy});
            endMap.erase({nextSeg->ex, nextSeg->ey});
        } else if (prevSeg) {
            // 只连接前面的线段
            segs[i].sx = prevSeg->sx;
            segs[i].sy = prevSeg->sy;
            segs[i].count = prevSeg->count + 1;
            
            startMap.erase({prevSeg->sx, prevSeg->sy});
            endMap.erase({prevSeg->ex, prevSeg->ey});
        } else if (nextSeg) {
            // 只连接后面的线段
            segs[i].ex = nextSeg->ex;
            segs[i].ey = nextSeg->ey;
            segs[i].count = 1 + nextSeg->count;
            
            startMap.erase({nextSeg->sx, nextSeg->sy});
            endMap.erase({nextSeg->ex, nextSeg->ey});
        }
        
        // 将当前（可能已合并的）线段加入映射
        startMap[{segs[i].sx, segs[i].sy}] = &segs[i];
        endMap[{segs[i].ex, segs[i].ey}] = &segs[i];
        
        // 更新最大值
        if (segs[i].count > maxCount) {
            maxCount = segs[i].count;
            maxX = segs[i].sx;
            maxY = segs[i].sy;
        }
    }
    
    cout << maxCount << " " << maxX << " " << maxY << endl;
    return 0;
}
