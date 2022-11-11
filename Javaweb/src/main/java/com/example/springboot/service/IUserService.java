package com.example.springboot.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.springboot.controller.dto.UserDTO;
import com.example.springboot.entity.User;

/**
 * <p>
 * 服务类
 * </p>
 *
 * @author jun
 * @since 2022-04-05
 */
public interface IUserService extends IService<User> {

    UserDTO login(UserDTO userDTO);

    User register(UserDTO userDTO);
}