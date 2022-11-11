package com.example.springboot.utils;

/**
 * @author zj
 * @date 2022/4/11 20:24
 */

import jxl.Workbook;
import jxl.write.Label;
import jxl.write.WritableSheet;
import jxl.write.WritableWorkbook;

import java.io.File;

public class CreateXLS {
    public static void main(String args[]) {
        try {
//打开文件
            WritableWorkbook book =
                    Workbook.createWorkbook(new File("测试.xls"));
//生成名为“第一页”的工作表，参数0表示这是第一页
            WritableSheet sheet = book.createSheet("sheet1", 0);
//在Label对象的构造子中指名单元格位置是第一列第一行(0,0)
//以及单元格内容为test
            for(int i = 1; i < 51; i++) {
                String chineseName = UserInfoAuto.getChineseName();
                String email = UserInfoAuto.getEmail();
                String tel = UserInfoAuto.getTel();
                String road = UserInfoAuto.getRoad();
                String pinyin = UserInfoAuto.testPinyin(chineseName);
                String password = UserInfoAuto.getPassword();
                Label label = new Label(0, i, pinyin);
//将定义好的单元格添加到工作表中
                sheet.addCell(label);
                label = new Label(1, i, password);
                sheet.addCell(label);
                label = new Label(2, i, chineseName);
                sheet.addCell(label);
                label = new Label(3, i, email);
                sheet.addCell(label);
                label = new Label(4, i, tel);
                sheet.addCell(label);
                label = new Label(5, i, road);
                sheet.addCell(label);
            }

//写入数据并关闭文件
            book.write();
            book.close();
        } catch(Exception e) {
            System.out.println(e);
        }
    }
}