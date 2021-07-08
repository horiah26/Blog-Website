import datetime
from models.post import Post

time_now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
post_list =[]

post1 = Post(1, "Lorem Ipsum", " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras at fringilla nisi. Suspendisse aliquam sapien quis mauris fermentum cursus. Nam eget metus efficitur, facilisis sapien in, sollicitudin arcu. Suspendisse dui elit, maximus a blandit et, porta eu odio. Vivamus euismod eros nulla. Pellentesque ultricies, neque ut vehicula tempus, nibh eros cursus odio, vitae lobortis lacus nibh et ligula. Aenean efficitur in quam sed hendrerit. Vestibulum consequat in nunc id tincidunt. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Praesent id fermentum ex. Fusce eu eleifend justo. Quisque non elementum sapien. Maecenas vulputate libero lacus, non commodo velit placerat rhoncus. Vivamus tristique, felis eget aliquam placerat, dolor lectus vehicula augue, non ultrices lorem sem a enim. Duis egestas orci non ultricies ullamcorper. Nullam sagittis mauris non felis blandit condimentum. Phasellus luctus finibus massa, non convallis justo varius in. Maecenas imperdiet dui nec lacus porta, non molestie nisl cursus. Sed sed imperdiet ex, in iaculis enim. In vitae ipsum eu sem scelerisque finibus vel sed neque. Curabitur a varius augue, id malesuada orci. Donec efficitur faucibus suscipit. Donec imperdiet, arcu vel convallis fermentum, quam lectus convallis purus, ut maximus justo nibh at nunc. Ut felis ligula, ornare vitae ornare non, maximus eu turpis. Quisque ac luctus sapien. Sed cursus augue ante, vel commodo augue auctor at. Phasellus varius risus ut ex malesuada mattis. Morbi ut turpis at tortor scelerisque malesuada. ", time_now, time_now)
post2 = Post(2, "Pellentesque tincidunt", " Quisque tempor fringilla velit et accumsan. Cras vitae purus sit amet tellus tempor facilisis. Quisque placerat euismod elit, euismod sollicitudin sem bibendum vitae. Duis sollicitudin, risus nec porttitor facilisis, lectus purus sodales nisi, accumsan sollicitudin eros nisl et diam. Curabitur vel lacinia elit. Suspendisse sollicitudin vehicula ante. Mauris nulla ipsum, eleifend in varius non, pellentesque non ex. Phasellus malesuada ullamcorper accumsan. Duis a sem maximus, vestibulum ligula ac, ultricies nisl. Ut vitae pretium nisi. Mauris lobortis dolor at lacus interdum, eget interdum magna bibendum. Quisque urna nulla, porttitor ac laoreet eget, lacinia vel elit. Nullam convallis massa a risus tincidunt tempus. Integer vestibulum pellentesque libero in dapibus. Nullam sed arcu in turpis congue rhoncus vitae vitae nulla. Sed in elit non justo faucibus suscipit. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Suspendisse commodo dictum lectus, at posuere magna hendrerit vitae. Sed faucibus ultrices lacus in pulvinar. Duis ex ante, pretium eu lorem eu, mollis aliquet diam. Phasellus erat est, dictum vitae consequat sit amet, mattis mollis felis. Pellentesque dapibus risus ante, nec molestie enim sagittis vel. Mauris mollis, diam et auctor varius, lacus ipsum dignissim purus, a commodo felis augue nec erat. Sed suscipit felis nec pretium ullamcorper. Etiam scelerisque lectus ultrices felis dapibus tincidunt. Fusce id mi quis velit lacinia suscipit in eu ante. Maecenas iaculis efficitur tristique. Mauris ultricies feugiat purus. Curabitur id ante vitae est eleifend egestas. ",time_now,time_now)
post3 = Post(3, "Aliquam at leo", " Duis risus nunc, consectetur sit amet justo sit amet, elementum auctor sem. Curabitur mi lectus, interdum a risus eget, volutpat auctor augue. Cras in nisi et ligula maximus aliquet. Duis rutrum pharetra faucibus. Morbi facilisis, metus nec porta congue, justo lacus pretium quam, a porta elit sem in mi. Morbi quis elementum lacus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas congue enim quis tempor dapibus. Cras consequat, magna id lobortis luctus, ligula sapien dapibus nunc, vel volutpat tortor leo nec velit. Proin facilisis quam sapien, eget suscipit nibh ultricies eu. Etiam a lacus cursus, tempus ligula quis, varius neque. In non turpis placerat, rutrum enim eget, vestibulum enim. Mauris quis tellus erat. Sed vel risus convallis, tempus felis et, lobortis ipsum. Sed volutpat vitae metus in consequat. Morbi luctus mauris eu lorem tincidunt, sed iaculis lorem pellentesque. Duis id turpis eleifend, vulputate ligula in, pellentesque odio. Sed condimentum leo dolor, porttitor pharetra est convallis sed. In hac habitasse platea dictumst. Duis ultricies porttitor dolor sit amet gravida. Vestibulum auctor, tellus id accumsan efficitur, enim felis dapibus justo, in rutrum mi enim et ipsum. Fusce quis lectus elit. Aliquam imperdiet odio id blandit consectetur. Ut scelerisque augue sit amet dui sodales tristique. Etiam in feugiat est. Nullam feugiat nec ex non egestas. Phasellus pretium iaculis ligula, nec gravida massa scelerisque in. Proin tristique molestie purus, eget dapibus purus ornare at. Pellentesque dapibus vitae felis ut eleifend.", time_now,time_now)
post4 = Post(4, "Duis a lectus", "Duis a lectus in erat blandit hendrerit eget quis purus. Duis eros nunc, pretium at aliquet a, feugiat sit amet nisl. Ut pharetra molestie euismod. Maecenas sed placerat mi. Fusce vel feugiat orci. Mauris convallis, erat non mollis sodales, libero lacus dapibus metus, quis facilisis ipsum orci sed nisi. Nam in ultricies ligula. Vivamus aliquam cursus ante ac porttitor. Phasellus iaculis, lectus eu fringilla imperdiet, ligula sapien pretium tellus, vel accumsan velit mauris quis nulla. Nunc scelerisque tincidunt semper. Curabitur vitae porta massa, nec posuere erat. Maecenas ultricies metus quis scelerisque ullamcorper. Maecenas efficitur lacinia sem, ac aliquet mi facilisis at. Proin at convallis ex. Integer dapibus, odio ac tempus malesuada, neque neque laoreet neque, ac maximus urna ipsum ut urna.", time_now, time_now)

post_list.append(post1)
post_list.append(post2)
post_list.append(post3)
post_list.append(post4)

