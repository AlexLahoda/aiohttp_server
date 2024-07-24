import asyncio
from aiohttp import web
from models import db, Apiuser, Location, Device
import logging

logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()


async def init_app():
    app = web.Application()
    app.add_routes(routes)
    return app


async def get_model(s):
    return globals()[s.title()]


@routes.view('/{table}')
class PostGetDevices(web.View):
    async def get(self):
        cls_name = self.request.match_info['table']
        model = await get_model(cls_name)
        devs = model.select()
        return web.json_response([dev.__data__ for dev in devs])

    async def post(self):
        try:
            cls_name = self.request.match_info['table']
            model = await get_model(cls_name)
            data = await self.request.json()
            row = model.create(**data)
            logging.info(f"Created {cls_name} with ID: {row.id}")
            return web.json_response({'id': row.id})
        except Exception as e:
            logging.error(f"Error while creating {cls_name}: {e}")
            return web.json_response({'error': str(e)}, status=500)
        

@routes.view('/{table}/{id}')
class GetUpdateDeleteDevice(web.View):
    async def get(self):
        cls_name = self.request.match_info['table']
        model = await get_model(cls_name)
        row = model.get_by_id(int(self.request.match_info['id']))
        return web.json_response(row.__data__)
    
    async def put(self):
        cls_name = self.request.match_info['table']
        model = await get_model(cls_name)
        row_id = int(self.request.match_info['id'])
        data = await self.request.json()
        model.update(**data).where(model.id == row_id).execute()
        return web.json_response({f'{cls_name.title()} {row_id} status: ': 'updated'})
    
    async def delete(self):
        cls_name = self.request.match_info['table']
        model = await get_model(cls_name)
        row_id = int(self.request.match_info['id'])
        model.delete_by_id(row_id)
        return web.json_response({f'{cls_name.title()} {row_id} status: ': 'deleted'})


if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    app = loop.run_until_complete(init_app())
    web.run_app(app, host='0.0.0.0', port=8080)