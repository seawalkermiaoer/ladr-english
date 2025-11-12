// api.ts

export interface LoginResponse {
  token: string;
  username: string;
  level: 'free' | 'plus' | 'pro';
}

export async function mockLogin(phone: string, password: string): Promise<LoginResponse> {
  console.log("Mock login:", phone, password);

  // 模拟网络延迟
  await new Promise((r) => setTimeout(r, 1000));

  if (password === "123456") {
    // Determine user level based on phone number
    let level: 'free' | 'plus' | 'pro' = 'free';
    const lastDigit = parseInt(phone.slice(-1));
    
    if (!isNaN(lastDigit)) {
      if (lastDigit <= 3) {
        level = 'free';
      } else if (lastDigit <= 6) {
        level = 'plus';
      } else {
        level = 'pro';
      }
    }
    
    return {
      token: `mock-token-${Date.now()}`,
      username: `User_${phone.slice(-4)}`,
      level: level
    };
  } else {
    throw new Error("手机号或密码错误");
  }
}

export async function mockFetchUserData(token: string) {
  if (!token.startsWith("mock-token")) throw new Error("Token 无效");
  return {
    nickname: "seawlaker",
    vip: true,
  };
}