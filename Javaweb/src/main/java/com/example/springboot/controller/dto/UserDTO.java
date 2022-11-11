package com.example.springboot.controller.dto;

import lombok.Data;

/**
 * @author zj
 * @date 2022/4/6 10:01
 * 接受前端登录请求的参数
 */
@Data
public class UserDTO {
    private String username;
    private String password;
    private String nickname;
    private String avatarUrl;
    private String token;
}
