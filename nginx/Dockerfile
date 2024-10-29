FROM nginx:stable-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

CMD ["nginx", "-g", "daemon off;"]

# COPY nginx/ca.crt /etc/nginx/ssl/ca.crt
# COPY nginx/your-domain.com.crt /etc/nginx/ssl/your-domain.com.crt
# COPY nginx/your-domain.com.key /etc/nginx/ssl/your-domain.com.key
