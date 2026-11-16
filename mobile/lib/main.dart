import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
const apiBaseUrl=String.fromEnvironment('API_BASE_URL',defaultValue:'http://10.0.2.2:8000/api');
const storage=FlutterSecureStorage();
void main()=>runApp(const SnapSpaceApp());
class SnapSpaceApp extends StatelessWidget {
 const SnapSpaceApp({super.key});
 @override Widget build(BuildContext context)=>MaterialApp(debugShowCheckedModeBanner:false,title:'SnapSpace',theme:ThemeData(colorScheme:ColorScheme.fromSeed(seedColor:const Color(0xFF7048D8)),useMaterial3:true,scaffoldBackgroundColor:const Color(0xFFF8F7FB)),home:const AuthScreen());
}
class AuthScreen extends StatefulWidget { const AuthScreen({super.key}); @override State<AuthScreen> createState()=>_AuthScreenState(); }
class _AuthScreenState extends State<AuthScreen> {
 final email=TextEditingController(),password=TextEditingController(),username=TextEditingController();
 bool login=true,busy=false; String message='';
 Future<void> submit() async {
  setState(()=>busy=true); message='';
  try {
   if(!login){final reg=await http.post(Uri.parse('$apiBaseUrl/auth/register/'),headers:{'Content-Type':'application/json'},body:jsonEncode({'email':email.text.trim(),'username':username.text.trim().toLowerCase(),'password':password.text}));if(reg.statusCode!=201)throw Exception(jsonDecode(reg.body).toString());}
   final res=await http.post(Uri.parse('$apiBaseUrl/auth/token/'),headers:{'Content-Type':'application/json'},body:jsonEncode({'username':login?email.text.trim():username.text.trim().toLowerCase(),'password':password.text}));
   if(res.statusCode!=200)throw Exception('Account created. Sign in using your username and password.');
   final data=jsonDecode(res.body) as Map<String,dynamic>;await storage.write(key:'access',value:data['access']);await storage.write(key:'refresh',value:data['refresh']);
   if(!mounted)return;Navigator.of(context).pushReplacement(MaterialPageRoute(builder:(_)=>const HomeScreen()));
  }catch(e){if(mounted)setState(()=>message=e.toString().replaceFirst('Exception: ',''));}finally{if(mounted)setState(()=>busy=false);}
 }
 @override Widget build(BuildContext context)=>Scaffold(body:Center(child:SingleChildScrollView(padding:const EdgeInsets.all(24),child:ConstrainedBox(constraints:const BoxConstraints(maxWidth:420),child:Card(elevation:0,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(26)),child:Padding(padding:const EdgeInsets.all(24),child:Column(crossAxisAlignment:CrossAxisAlignment.stretch,children:[
 const Text('snapspace ✦',style:TextStyle(fontSize:30,fontWeight:FontWeight.w900,color:Color(0xFF7048D8))),const SizedBox(height:12),Text(login?'Welcome back':'Create your space',style:Theme.of(context).textTheme.headlineMedium),
 if(!login)TextField(controller:username,decoration:const InputDecoration(labelText:'Username',border:OutlineInputBorder())),
 const SizedBox(height:12),TextField(controller:email,decoration:const InputDecoration(labelText:'Email',border:OutlineInputBorder())),const SizedBox(height:12),TextField(controller:password,obscureText:true,decoration:const InputDecoration(labelText:'Password',border:OutlineInputBorder())),
 if(message.isNotEmpty)Padding(padding:const EdgeInsets.all(8),child:Text(message,style:const TextStyle(color:Colors.red))),
 FilledButton(onPressed:busy?null:submit,child:Text(busy?'Please wait…':login?'Log in':'Create account')),TextButton(onPressed:busy?null:()=>setState(()=>login=!login),child:Text(login?'New here? Create account':'Already registered? Log in'))
 ])))))));
 }
}
class HomeScreen extends StatefulWidget { const HomeScreen({super.key}); @override State<HomeScreen> createState()=>_HomeScreenState(); }
class _HomeScreenState extends State<HomeScreen> {
 int tab=0;bool loading=true;String error='';List<dynamic> posts=[];
 @override void initState(){super.initState();loadFeed();}
 Future<void> loadFeed() async {
 setState(()=>loading=true);
 try{final token=await storage.read(key:'access');final res=await http.get(Uri.parse('$apiBaseUrl/posts/'),headers:{'Authorization':'Bearer $token'});if(res.statusCode!=200)throw Exception('Feed request failed (${res.statusCode})');final body=jsonDecode(res.body);setState(()=>posts=body is List?body:(body['results'] as List? ?? []));}
 catch(e){setState(()=>error=e.toString());}finally{if(mounted)setState(()=>loading=false);}
 }
 @override Widget build(BuildContext context)=>Scaffold(appBar:AppBar(title:const Text('snapspace ✦',style:TextStyle(fontWeight:FontWeight.w900,color:Color(0xFF7048D8))),actions:[IconButton(onPressed:loadFeed,icon:const Icon(Icons.refresh))]),body:loading?const Center(child:CircularProgressIndicator()):error.isNotEmpty?Center(child:Text(error)):RefreshIndicator(onRefresh:loadFeed,child:ListView(padding:const EdgeInsets.all(14),children:[
 const Card(child:Padding(padding:EdgeInsets.all(18),child:Text('Your world. Your people. Share a moment ✨'))),
 for(final post in posts)Card(margin:const EdgeInsets.only(top:14),clipBehavior:Clip.antiAlias,child:Padding(padding:const EdgeInsets.all(14),child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
 Text('@${post['user']?['profile']?['username']??'member'}',style:const TextStyle(fontWeight:FontWeight.bold)),const SizedBox(height:10),
 if(post['media_url']!=null)Image.network(post['media_url'],fit:BoxFit.cover,errorBuilder:(_,__,___)=>const SizedBox(height:120,child:Center(child:Text('Media unavailable')))),
 const SizedBox(height:8),Text(post['caption']??''),const SizedBox(height:8),Text('♥ ${post['like_count']??0}  ·  ${post['comment_count']??0} comments')
 ]))))
 ])),bottomNavigationBar:NavigationBar(selectedIndex:tab,onDestinationSelected:(v)=>setState(()=>tab=v),destinations:const [NavigationDestination(icon:Icon(Icons.home_outlined),label:'Home'),NavigationDestination(icon:Icon(Icons.search),label:'Explore'),NavigationDestination(icon:Icon(Icons.video_library_outlined),label:'Reels'),NavigationDestination(icon:Icon(Icons.person_outline),label:'Profile')]));
 }
}
