import pandas as pd
import numpy as np
from dash import no_update

def controlShape_Tab(retrieve,firstchoosen, secondchoosen,firstshape, leftfirstval,leftsecondval,secondshape,
                 rightfirstval,rightsecondval,minValfirst, minValsecond):
    if retrieve != []:
        df = pd.DataFrame(retrieve)
        df['index'] = df.index
        df = df.reindex(columns=sorted(df.columns, reverse=True))
        baseval = ''
        if 'date' not in df.columns:
            for col in df.columns:
                if 'Temps' in col:
                    baseval += col
                    dt = df[baseval]
                    print('bu dt nedir', dt)
            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                dff = df[df['ID'] == firstchoosen[-1]]
                dff = dff.copy()
                index = np.arange(0, len(dff['ID']))
                dff.reset_index(drop=True, inplace=True)
                dff.set_index(index, inplace=True)
                dt = dff[['Date']]
                dt.columns = ['Date']
                dt = dt['Date'].apply(lambda x: x[:10] + '_' + x[12:])

                dff2 = df[df['ID'] == secondchoosen]
                dff2 = dff2.copy()
                index = np.arange(0, len(dff2['ID']))
                dff2.reset_index(drop=True, inplace=True)
                dff2.set_index(index, inplace=True)
                dt2 = dff2[['Date']]
                dt2.columns = ['Date']
                dt2 = dt2['Date'].apply(lambda x: x[:10] + '_' + x[12:])

        if 'date' in df.columns:
            if type(df['date'][0]) == 'str':
                df_shape = df.copy()
                df_shape['newindex'] = df_shape.index
                df_shape.index = df_shape['date']
                dt = ["{}-{:02.0f}-{:02.0f}_{:02.0f}:{:02.0f}:{:02.0f}".format(d.year, d.month, d.day, d.hour, d.minute,
                                                                               d.second) for d in df_shape.index]

            else:
                dt = df['date']

    pathline = ''
    pathline2 = ''
    df = pd.DataFrame(retrieve)
    if firstchoosen[-1] != None and secondchoosen != None:
        if len(firstshape) == 2 and leftfirstval != None and leftsecondval != None:
            if int(firstshape[1]) > int(firstshape[0]):
                pathline = ''
                rangeshape = range(int(firstshape[0]), int(firstshape[1]) + 2)
                print('rangeshape', rangeshape)
                if ':' or '-' in dt[0]:

                    for k in rangeshape:
                        print('biiiiiiiiiiiiiiiir', k)
                        if k == rangeshape[0]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += 'M ' + dt[k] + ', ' + str(minValfirst) + ' L' + \
                                            dt[k] + ', ' + str(list(dff[dff.index == k]['Value'])[0]) + ' '
                                print('pathline1', pathline)
                            else:
                                pathline += 'M ' + str(dt[k]) + ', ' + str(minValfirst) + ' L' + str(
                                    dt[k]) + ', ' + str(df[firstchoosen[-1]][k]) + ' '
                                print('pathline2', pathline)

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += ' L' + dt[k] + ', ' + str(list(dff[dff.index == k]['Value'])[0])
                                print('pathline3', pathline)
                                print('pathline3', k)

                            else:
                                pathline += ' L' + str(dt[k]) + ', ' + str(df[firstchoosen[-1]][k])
                                print('pathline3', pathline)
                        elif k == rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += ' L' + dt[k - 1] + ', ' + str(minValfirst)
                                pathline += ' Z'
                                print('pathline4', pathline)
                                print('burasi 1')
                            else:
                                pathline += ' L' + str(dt[k - 1]) + ', ' + str(minValfirst)
                                pathline += ' Z'
                                print('pathline4', pathline)
                                print('burasi 2')
                else:
                    print('333333')
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            pathline += 'M ' + str(dt[k]) + ', ' + str(minValfirst) + ' L' + \
                                        str(dt[k]) + ', ' + str(df[firstchoosen[-1]][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            pathline += ' L' + str(int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k])
                    pathline += ' L' + str(int(dt[k - 1])) + ', ' + str(minValfirst)
                    pathline += ' Z'

        if len(secondshape) == 2 and rightsecondval != None and rightfirstval != None:
            if int(secondshape[1]) > int(secondshape[0]):
                rangeshape = range(int(secondshape[0]), int(secondshape[1] + 2))
                if ':' or '-' in dt[0]:
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += 'M ' + dt2[k] + ', ' + str(minValfirst) + ' L' + \
                                             dt2[k] + ', ' + str(list(dff2[dff2.index == k]['Value'])[0]) + ' '
                                print('pathline1', pathline)
                            else:
                                pathline2 += 'M ' + str(dt[k]) + ', ' + str(minValsecond) + ' L' + str(
                                    dt[k]) + ', ' + str(df[secondchoosen][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += ' L' + dt2[k] + ', ' + str(list(dff2[dff2.index == k]['Value'])[0])
                                print('pathline3', pathline)
                            else:
                                pathline2 += ' L' + str(dt[k]) + ', ' + str(df[secondchoosen][k])
                        elif k == rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += ' L' + dt2[k - 1] + ', ' + str(minValfirst)
                                pathline2 += ' Z'
                                print('pathline4', pathline)
                                print('burasi 1')
                            else:
                                pathline2 += ' L' + str(dt[k - 1]) + ', ' + str(minValsecond)
                                pathline2 += ' Z'
                else:
                    for k in rangeshape:

                        if k == rangeshape[0]:
                            pathline2 += 'M ' + str(dt[k]) + ', ' + str(minValsecond) + ' L' + str(
                                dt[k]) + ', ' + str(df[secondchoosen][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            pathline2 += ' L' + str(int(dt[k])) + ', ' + str(df[secondchoosen][k])
                    pathline2 += ' L' + str(int(dt[k - 1])) + ', ' + str(minValsecond)
                    pathline2 += ' Z'

        return [dict(
            type="path",
            path=pathline,
            layer='below',
            fillcolor="#5083C7",
            opacity=0.8,
            line_color="#8896BF",
        ), dict(
            type="path",
            path=pathline2,
            layer='below',
            fillcolor="#B0384A",
            opacity=0.8,
            line_color="#B36873",
        )]

    if firstchoosen[-1] != None and secondchoosen == None:
        if len(firstshape) == 2:
            if int(firstshape[1]) > int(firstshape[0]) or int(firstshape[0]) > int(firstshape[1]):
                pathline = ''
                rangeshape = range(int(firstshape[0]), int(firstshape[1]) + 2)
                print('rangeshape', rangeshape)
                if ':' or '-' or '_' in dt[0]:
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += 'M ' + dt[k] + ', ' + str(minValfirst) + ' L' + \
                                            dt[k] + ', ' + str(list(dff[dff.index == k]['Value'])[0]) + ' '
                                print('pathline1', pathline)
                            else:
                                pathline += 'M ' + str(dt[k]) + ', ' + str(minValfirst) + ' L' + str(
                                    dt[k]) + ', ' + str(df[firstchoosen[-1]][k]) + ' '
                                print('pathline2', pathline)

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += ' L' + dt[k] + ', ' + str(list(dff[dff.index == k]['Value'])[0])
                                print('pathline3', pathline)

                            else:
                                pathline += ' L' + str(dt[k]) + ', ' + str(df[firstchoosen[-1]][k])
                                print('pathline3', pathline)
                        elif k == rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline += ' L' + dt[k - 1] + ', ' + str(minValfirst)
                                pathline += ' Z'
                                print('pathline4', pathline)
                                print('burasi 1')
                            else:
                                pathline += ' L' + str(dt[k - 1]) + ', ' + str(minValfirst)
                                pathline += ' Z'
                                print('pathline4', pathline)
                                print('burasi 2')
                else:
                    print('buraya mi geciyor yoksa')
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            pathline += 'M ' + str(dt[k]) + ', ' + str(minValfirst) + ' L' + \
                                        str(dt[k]) + ', ' + str(df[firstchoosen[-1]][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            pathline += ' L' + str(int(dt[k])) + ', ' + str(df[firstchoosen[-1]][k])
                    pathline += ' L' + str(int(dt[k - 1])) + ', ' + str(minValfirst)
                    pathline += ' Z'

            return [dict(
                type="path",
                path=pathline,
                layer='below',
                fillcolor="#5083C7",
                opacity=0.8,
                line_color="#8896BF",
            )]

    if secondchoosen != None and firstchoosen[-1] == None:
        if len(secondshape) == 2 and rightsecondval != None and rightfirstval != None:
            if int(secondshape[1]) > int(secondshape[0]) or int(secondshape[0]) > int(secondshape[1]):
                rangeshape = range(int(secondshape[0]), int(secondshape[1]) + 2)
                if ':' or '-' in dt[0]:
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += 'M ' + dt2[k] + ', ' + str(minValfirst) + ' L' + \
                                             dt2[k] + ', ' + str(list(dff2[dff2.index == k]['Value'])[0]) + ' '
                                print('pathline1', pathline)
                            else:
                                pathline2 += 'M ' + str(dt[k]) + ', ' + str(minValsecond) + ' L' + str(
                                    dt[k]) + ', ' + str(df[secondchoosen][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += ' L' + dt2[k] + ', ' + str(list(dff2[dff2.index == k]['Value'])[0])
                                print('pathline3', pathline)
                            else:
                                pathline2 += ' L' + str(dt[k]) + ', ' + str(df[secondchoosen][k])
                        elif k == rangeshape[-1]:
                            if 'ID' and 'Value' and 'Quality' and 'Date' in df.columns:
                                pathline2 += ' L' + dt2[k - 1] + ', ' + str(minValfirst)
                                pathline2 += ' Z'
                                print('pathline4', pathline)
                                print('burasi 1')
                            else:
                                pathline2 += ' L' + str(dt[k - 1]) + ', ' + str(minValsecond)
                                pathline2 += ' Z'
                else:
                    for k in rangeshape:
                        if k == rangeshape[0]:
                            pathline2 += 'M ' + str(dt[k]) + ', ' + str(minValsecond) + ' L' + str(
                                dt[k]) + ', ' + str(df[secondchoosen][k]) + ' '

                        elif k != rangeshape[0] and k != rangeshape[-1]:
                            pathline2 += ' L' + str(int(dt[k])) + ', ' + str(df[secondchoosen][k])
                    pathline2 += ' L' + str(int(dt[k - 1])) + ', ' + str(minValsecond)
                    pathline2 += ' Z'

            return [dict(
                type="path",
                path=pathline2,
                layer='below',
                fillcolor="#5083C7",
                opacity=0.8,
                line_color="#8896BF",
            )]


